import requests
import os
import random


class LoveQuoteFetcher:
    """
    用于从天API获取随机情话的类。

    属性:
        api_key (str): 用于访问天API的API密钥。
        quote_urls (list): 包含两个URL的列表，分别用于获取情话和彩虹屁。
    """

    def __init__(self):
        """
        初始化LoveQuoteFetcher实例。

        初始化时会从环境变量中获取TIAN_KEY。如果环境变量未设置，
        将抛出一个ValueError异常。
        """
        self.api_key = os.environ.get('TIAN_KEY')
        if not self.api_key:
            raise ValueError("TIAN_KEY 环境变量必须设置。")
        self.quote_urls = [
            f'https://apis.tianapi.com/saylove/index?key={self.api_key}',
            f'https://apis.tianapi.com/caihongpi/index?key={self.api_key}'
        ]

    def get_random_quote(self):
        """
        获取一条随机的情话。

        :return: 如果请求成功，则返回随机情话的字符串；否则返回None。
        """
        # 随机选择一个URL
        selected_url = random.choice(self.quote_urls)

        try:
            # 发送HTTP GET请求
            response = requests.get(selected_url)

            # 检查请求是否成功
            if response.status_code == 200:
                # 解析返回的JSON数据
                quote_data = response.json()
                # 打印返回的json数据
                print(quote_data)

                # 尝试从返回的数据中提取情话内容，提供一个默认值，若无数据则返回空字典{}
                content = quote_data.get('result', {}).get('content')

                # 如果找到了内容，返回去除空白字符的内容
                if content is not None:
                    return f"致亲爱的老婆：{content.strip()}"

                # 如果没有找到content字段，打印提示信息
                print("返回的数据中没有找到'content'字段")

        except Exception as e:
            # 如果发生异常，打印错误信息
            print(f"发生错误：{e}")

        # 请求失败或未找到内容时返回None
        return None


class EmailNotifier:
    """
    使用PushPlus服务发送邮件通知的类。

    属性:
        token (str): 用于访问PushPlus服务的Token。
        url (str): PushPlus API的URL。
    """

    def __init__(self):
        """
        初始化EmailNotifier实例。

        初始化时会从环境变量中获取PUSHPLUS_TOKEN。如果环境变量未设置，
        将抛出一个ValueError异常。
        """
        self.token = os.environ.get('PUSHPLUS_TOKEN')
        if not self.token:
            raise ValueError("PUSHPLUS_TOKEN 环境变量必须设置。")
        self.url = "http://www.pushplus.plus/send"

    def send_email(self, title, content):
        """
        发送带有指定标题和内容的邮件。

        :param title: 邮件标题
        :param content: 邮件内容
        """
        # 构建发送邮件所需的数据字典
        data = {
            "token": self.token,  # 推送使用的Token
            "title": title,  # 邮件标题
            "content": content,  # 邮件内容
            # "topic": "wkwlp",  # 群组编码
            "template": "txt",  # 使用的邮件模板，此处使用纯文本格式
            "channel": "mail"  # 指定推送方式为邮件
        }

        # 设置请求头，告知服务器我们将发送JSON格式的数据
        headers = {'Content-Type': 'application/json'}

        # 使用POST方法发送数据，并获取响应对象
        response = requests.post(self.url, json=data, headers=headers)

        # 判断请求是否成功
        if response.status_code == 200:  # 如果状态码是200，则请求成功
            print("邮件提醒发送成功")
        else:  # 如果状态码不是200，则请求失败
            print(f"邮件提醒发送失败，状态码：{response.status_code}")


def main():
    """
    主函数，用于执行获取随机情话并发送邮件提醒的流程。

    :return: 无返回值
    """
    # 创建情话获取器实例
    quote_fetcher = LoveQuoteFetcher()

    # 获取随机情话
    quote = quote_fetcher.get_random_quote()

    if quote:
        # 创建邮件通知器实例
        email_notifier = EmailNotifier()

        # 发送邮件提醒
        email_notifier.send_email('每日小情话', quote)


if __name__ == "__main__":
    main()