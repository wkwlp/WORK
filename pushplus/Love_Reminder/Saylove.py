import requests
import os
import random
import logging
from pushplus.common import *

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(threadName)s] %(name)s.%(funcName)s:%(lineno)d - %(message)s'
)

class LoveQuoteFetcher:
    """
    用于从天API获取随机情话的类。

    属性:
        api_key (str): 用于访问天API的API密钥。
        quote_urls (list): 包含两个URL的列表，分别用于获取情话和彩虹屁。
    """
    logger = logging.getLogger(__name__)  # 创建一个与当前模块同名的日志记录器

    def __init__(self):
        """
        初始化LoveQuoteFetcher实例。

        初始化时会从环境变量中获取TIAN_KEY。如果环境变量未设置，
        将抛出一个ValueError异常。
        """
        self.api_key = os.environ.get('TIAN_KEY')
        if not self.api_key:
            raise ValueError("TIAN_KEY 环境变量未设置。")
        self.quote_urls = [
            f'https://apis.tianapi.com/saylove/index?key={self.api_key}',
            f'https://apis.tianapi.com/caihongpi/index?key={self.api_key}'
        ]
        self.logger.info("LoveQuoteFetcher 初始化完成")

    def get_random_quote(self):
        """
        获取一条随机的情话。

        :return: 如果请求成功，则返回随机情话的字符串；否则返回None。
        """
        # 随机选择一个URL
        selected_url = random.choice(self.quote_urls)

        self.logger.info(f"选择的URL: {selected_url.replace(self.api_key, '[SENSITIVE_DATA]', 1)}")

        try:
            # 发送HTTP GET请求
            response = requests.get(selected_url)

            # 检查请求是否成功
            if response.status_code == 200:
                # 解析返回的JSON数据
                quote_data = response.json()
                self.logger.info(f"收到的响应: {quote_data}")

                # 尝试从返回的数据中提取情话内容，提供一个默认值，若无数据则返回空字典{}
                content = quote_data.get('result', {}).get('content')

                # 如果找到了内容，返回去除空白字符的内容
                if content is not None:
                    return f"致亲爱的老婆：{content.strip()}"

                # 如果没有找到content字段，打印提示信息
                self.logger.warning("返回的数据中没有找到'content'字段")

        except Exception as e:
            # 如果发生异常，打印错误信息
            self.logger.error(f"发生错误：{e}")

        # 请求失败或未找到内容时返回None
        return None


def main():
    """
    主函数，用于执行获取随机情话并发送邮件提醒的流程。

    :return: 无返回值
    """
    logger = logging.getLogger(__name__)  # 创建一个与当前模块同名的日志记录器

    # 创建情话获取器实例
    quote_fetcher = LoveQuoteFetcher()

    # 过滤的值列表
    custom_values = ["嫁你", "嫁给你","像你"]

    # 获取随机情话，并确保不包含自定义的值
    quote = quote_fetcher.get_random_quote()
    while any(value in quote for value in custom_values):
        quote = quote_fetcher.get_random_quote()

    logger.info(f"获取的情话: {quote}")

    if quote:
        # 创建邮件通知器实例
        email_notifier = SendEmail()

        # 发送邮件提醒
        email_notifier.send_reminder_email('每日小情话', quote,is_group_send=True)


if __name__ == "__main__":
    main()