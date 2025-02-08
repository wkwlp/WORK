import requests
import os
from pushplus.config import *
from fuzzywuzzy import process


class WeatherApi:
    """
    用于从高德地图API获取天气信息的类。
    """

    def __init__(self, content: str = None):
        """
        初始化WeatherApi实例。

        从配置文件中读取API URL、城市列表、气象类型等参数，并从环境变量中获取API密钥。

        参数:
        - content (str): 用户提供的城市名称，默认为None。如果未提供，则记录错误日志。
        """
        # 创建一个与当前模块同名的日志记录器
        self.logger = setup_logger()

        reader = ConfigReader()
        # 读取配置文件中的URL和其他参数
        weather_config = reader.get_weather_config()

        self.url = weather_config.get('URL')
        self.city = weather_config.get('City')
        self.extension = weather_config.get('Extension')
        self.output = weather_config.get('Output')[0]
        if content is None:
            self.logger.error("未提供城市名称")
        self.content = content

        self.weather_key = os.getenv('Weather_Key')
        if not self.weather_key:
            raise ValueError("未设置 Weather_Key 环境变量")

    def _handle_input(self) -> (str, str):
        """
        处理输入的城市名称和气象类型，进行模糊匹配并返回相应的编码。

        返回:
        - tuple: 包含(city_code, extension_code)，如果匹配失败则返回(None, None)。
        """
        city_key = list(self.city.keys())
        extension_key = list(self.extension.keys())
        if self.content is None:
            return None, None
        # 模糊匹配城市名称
        city_name, score2 = process.extractOne(self.content, extension_key)
        # 模糊匹配气象名称
        extension_name, score1 = process.extractOne(self.content, city_key)
        self.logger.info(
            f"城市匹配结果: {city_name}, 相似度得分: {score2}, 气象匹配结果: {extension_name}, 相似度得分: {score1}")

        # 如果相似度得分低于某个阈值，认为匹配失败
        if score1 < 20:
            self.logger.error(f"无法找到足够相似的位置名称: {self.content}")
            return None, None

        return self.city[extension_name], self.extension[city_name]

    def _set_url(self, output=None) -> str:
        """
        根据城市编码和扩展类型编码构建完整的天气查询URL。

        参数:
        - output (str): 输出格式，默认为None，如果未提供则使用self.output。

        返回:
        - 完整的URL字符串。
        """
        # 如果没有传入output参数，则使用self.output作为默认值
        if output is None:
            output = self.output

        # 处理输入内容以获取city_code和extension_code
        city_code, extension_code = self._handle_input()

        # 构建完整的URL
        complete_url = f"{self.url}?city={city_code}&key={self.weather_key}&extensions={extension_code}&output={output}"

        # 记录日志并隐藏敏感信息
        self.logger.info(f"完整的url: {complete_url.replace(self.weather_key, '[SENSITIVE_DATA]', 1)}")

        return complete_url

    def get_weather_condition(self) -> dict or None:
        """
        获取指定城市的天气状况。

        返回:
        - dict: 包含状态码、消息和天气数据。如果请求失败或未获取到天气数据，则返回错误信息或None。
        """
        complete_url = self._set_url()

        try:
            # 发送HTTP GET请求
            response = requests.get(complete_url)
            self.logger.info(f"发送的请求: {response}")
            # 检查请求是否成功
            if response.status_code == 200:
                # 解析返回的JSON数据
                weather_data = response.json()
                self.logger.info(f"收到的响应: {weather_data}")
                # 返回获取到的数据
                if weather_data.get('lives') or weather_data.get('forecasts'):
                    return {'status': 200, 'message': '天气状况获取成功', 'weather_data': weather_data}
                else:
                    return {'status': 400, 'message': '未获取到天气状况'}

            else:
                self.logger.error(f"请求失败，状态码：{response.status_code}")
        except Exception as e:
            self.logger.error(f"发生错误：{e}")
            return None


if __name__ == '__main__':
    weather_api = WeatherApi()
    weather_data = weather_api.get_weather_condition()
    print(weather_data)