import requests
import os
import random
import send
import json

class LoveQuoteApi:
    """
    用于从天API获取随机情话的类。

    属性:
        CalendarKEY (str): 用于访问天API的API密钥。
        quote_urls (list): 包含两个URL的列表，分别用于获取情话和彩虹屁。
    """

    def __init__(self):
        """
        初始化LoveQuoteApi实例，从config.ini文件中读取API URL，并从环境变量中获取API密钥。
        """

        self.logger = send.setup_logger()
        self.api_key = os.getenv('TIAN_KEY')
        if not self.api_key:
            self.logger.error("未设置 TIAN_KEY 环境变量")
            raise ValueError("未设置 TIAN_KEY 环境变量")
        self.love_mysql = send.LoveMysql()
        results = self.love_mysql.select_love_url()
        if not results:
            self.logger.error("数据库中没有获取到URL")
        say_love_url, cai_hong_pi_url = results[0], results[1]
        self.quote_urls = [
            {"type": "say_love", "url": f"{say_love_url}?key={self.api_key}"},
            {"type": "cai_hong_pi", "url": f"{cai_hong_pi_url}?key={self.api_key}"}
        ]
    def get_random_quote(self):
        """
        获取一条随机的情话。

        :return: 如果请求成功，则返回包含情话内容的字典；否则返回None。
        """
        # 随机选择一个URL
        selected_quote = random.choice(self.quote_urls)
        selected_url = selected_quote["url"]

        try:
            # 发送HTTP GET请求
            response = requests.get(selected_url)

            # 检查请求是否成功
            if response.status_code == 200:
                # 解析返回的JSON数据
                quote_data = response.json()
                self.logger.info(f"RESPONSE: {quote_data}")
                data = json.dumps(quote_data,ensure_ascii=False)

                if selected_quote["type"] == "say_love":
                    hzbh =self.love_mysql.insert_love_api(url_name='情话',response=data)
                    self.love_mysql.insert_love_hz(hzbh=hzbh,fszt='F00')
                    if hzbh:
                        return hzbh,quote_data
                else:
                    hzbh = self.love_mysql.insert_love_api(url_name='彩虹屁',response=data)
                    self.love_mysql.insert_love_hz(hzbh=hzbh,fszt='F00')
                    if hzbh:
                        return hzbh,quote_data
            else:
                self.logger.error(f"请求失败，状态码：{response.status_code}")
        except Exception as e:
            self.logger.error(f"发生错误：{e}")

        # 请求失败返回None
        self.logger.error("请求失败，返回空")
        return None

if __name__ == '__main__':
    a = LoveQuoteApi()
    a.get_random_quote()
