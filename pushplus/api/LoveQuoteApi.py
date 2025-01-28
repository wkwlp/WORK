import requests
import os
import random
import logging
import configparser
from pathlib import Path

class LoveQuoteApi:
    """
    用于从天API获取随机情话的类。

    属性:
        api_key (str): 用于访问天API的API密钥。
        quote_urls (list): 包含两个URL的列表，分别用于获取情话和彩虹屁。
    """
    logger = logging.getLogger(__name__)  # 创建一个与当前模块同名的日志记录器

    def __init__(self):
        """
        初始化LoveQuoteApi实例，从config.ini文件中读取API URL，并从环境变量中获取API密钥。
        """
        # 使用相对路径读取配置文件
        config_path = Path(__file__).resolve().parents[1] / 'config.ini'
        config = configparser.ConfigParser()
        config.read(config_path)

        self.api_key = os.getenv('TIAN_KEY')
        if not self.api_key:
            raise ValueError("未设置 TIAN_KEY 环境变量")

        # 读取配置文件中的URL
        self.say_love_url = config['LoveQuoteConfig']['SayLoveURL']
        self.cai_hong_pi_url = config['LoveQuoteConfig']['CaiHongPiURL']

        # 构建完整的URL
        self.quote_urls = [
            f"{self.say_love_url}?key={self.api_key}",
            f"{self.cai_hong_pi_url}?key={self.api_key}"
        ]

        self.logger.info("LoveQuoteApi 初始化完成")

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
        return None