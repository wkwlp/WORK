import os
from pushplus.config.logger_config import setup_logger
import requests
import re
from pushplus.config import *
from datetime import datetime
from lunardate import LunarDate

class EventApi:
    """
    用于从聚合数据获取指定日期的日历信息的类。

    属性:
        CalendarKEY (str): 用于访问聚合数据的API密钥。
        CalendarURL (str): 获取日历信息的API URL。
    """
    logger = setup_logger()

    def __init__(self):
        """
        初始化EventApi实例，从config.ini文件中读取API URL，并从环境变量中获取API密钥。
        """
        reader = ConfigReader()
        # 读取配置文件
        event_config = reader.get_event_config()
        # 读取配置文件中的URL
        self.CalendarURL = event_config['CalendarURL']

        self.CalendarKEY = os.getenv('CalendarKEY')
        if not self.CalendarKEY:
            raise ValueError("未设置 CalendarKEY 环境变量")

        # 初始化当前日期
        self.today = datetime.today()

    def get_calendar(self, date: str) -> dict or None:
        """
        获取指定日期的详细日历信息。
        参数:
            date (str): 格式为YYYY-MM-DD,如月份和日期小于10,则取个位,如:2012-1-1
        返回:
            返回一个包含日历信息的字典(dict)；
            如果请求失败或发生异常，则返回None。
        """
        # 检查参数类型是否为字符串
        if not isinstance(date, str):
            self.logger.error(f"无效的参数类型: {type(date)}, 应为字符串")
            return None

        # 正则表达式匹配 YYYY-M-D 格式的日期，不接受月份和日期有前导零
        if not re.match(r'^\d{4}-(1[0-2]|[1-9])-(3[01]|[12]\d|[1-9])$', date):
            self.logger.error(f"无效的日期格式: {date}, 月份和日期不应包含前导零")
            return None

        # 构造请求参数
        request_params = {
            'key': self.CalendarKEY,
            'date': date
        }

        try:
            # 发送HTTP GET请求
            response = requests.get(self.CalendarURL, params=request_params)

            # 检查请求是否成功
            if response.status_code == 200:
                # 解析返回的JSON数据
                calendar_data = response.json()
                self.logger.info(f"收到的响应: {calendar_data}")

                # 检查 result 字段是否存在且不为 None
                if 'result' not in calendar_data or calendar_data['result'] is None:
                    self.logger.error("API响应中未找到有效的result")
                    return None

                # 返回获取到的数据
                return calendar_data
            else:
                self.logger.error(f"请求失败，状态码：{response.status_code}")
        except Exception as e:
            self.logger.error(f"发生错误：{e}")

        # 请求失败返回None
        return None

    def get_lunar_date(self) -> str:
        """
        获取今天的农历月份和日期，并以 'x月x日' 的格式返回。

        :return: str, 农历月份和日期
        """
        # 将今天的阳历日期转换为农历日期
        lunar_date = LunarDate.fromSolarDate(self.today.year, self.today.month, self.today.day)
        # 格式化农历日期为 'x月x日' 格式
        formatted_lunar_date = f"{lunar_date.month}月{lunar_date.day}日"
        self.logger.info("获取到今天的农历日期: %s", formatted_lunar_date)
        return formatted_lunar_date


if __name__ == '__main__':
    api = EventApi()
    # 测试获取日历信息
    print(api.get_calendar('2023-7-1'))
    # 测试获取农历日期
    print(api.get_lunar_date())