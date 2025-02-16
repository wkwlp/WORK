import requests
import os
import random
import send

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
        reader = send.ConfigReader()
        # 读取配置文件中的URL
        love_quote_config = reader.get_love_quote_config()
        self.say_love_url, self.cai_hong_pi_url = love_quote_config['SayLoveURL'], love_quote_config['CaiHongPiURL']

        self.api_key = os.getenv('TIAN_KEY')
        if not self.api_key:
            raise ValueError("未设置 TIAN_KEY 环境变量")
        # 构建完整的URL

        self.quote_urls = [
            f"{self.say_love_url}?key={self.api_key}",
            f"{self.cai_hong_pi_url}?key={self.api_key}"
        ]


    def get_random_quote(self):
        """
        获取一条随机的情话。

        :return: 如果请求成功，则返回包含情话内容的字典；否则返回None。
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
                # 返回获取到的数据
                return quote_data
            else:
                self.logger.error(f"请求失败，状态码：{response.status_code}")
        except Exception as e:
            self.logger.error(f"发生错误：{e}")

        # 请求失败返回None
        self.logger.error("请求失败，返回空")
        return None

a = LoveQuoteApi()
print(a.get_random_quote())