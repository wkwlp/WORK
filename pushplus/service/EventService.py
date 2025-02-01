from datetime import datetime, timedelta
import lunardate
from pushplus.logger_config import setup_logger
from pushplus.api import *
from pushplus.config import *

class EventService:
    """
    处理从API获取的日历信息的服务类。

    该类负责调用外部API获取指定日期的日历信息，并对返回的数据进行处理，最终返回格式化后的日历内容。
    """
    logger = setup_logger()  # 创建一个与当前模块同名的日志记录器

    def __init__(self):
        """
        初始化EventService实例。

        在初始化时，会创建一个EventApi实例用于后续获取日历数据。
        """
        reader = ConfigReader()
        event_config = reader.get_event_config()
        self.event_days= event_config['EventDays']
        self.current_year = datetime.now().year
        self.event_api = EventApi()

    def get_calendar(self, query_date: str = None) -> tuple or None:
        """
        获取并处理指定日期的日历信息。

        参数:
            query_date (str, optional): 格式为YYYY-MM-DD,如月份和日期小于10,则取个位,如:2012-1-1。
                如果未提供，则默认使用明天的日期。

        返回:
            如果请求成功，则返回一个包含日期和节日的元组(date, holiday)，其中：
                - date (str): 查询的日期，格式为YYYY-MM-DD,如月份和日期小于10,则取个位,如:2012-1-1
                - holiday (str): 当天的节日名称。
            如果请求失败或发生异常，则返回(None, None)。
        """
        try:
            # 如果未提供 query_date，则使用明天的日期
            if query_date is None:
                tomorrow = datetime.today() + timedelta(days=1)
                # 先格式化为带前导零的日期，再去掉前导零
                query_date = tomorrow.strftime('%Y-%m-%d').replace('-0', '-')
                self.logger.info("未提供日期，使用明天的日期: %s", query_date)

            # 调用API获取日历数据
            calendar_data = self.event_api.get_calendar(query_date)

            # 处理获取到的日历数据
            date_info, holiday_info = self.handle_calendar(calendar_data)
            calendar_content = {"date":date_info,"holiday":holiday_info}
            return calendar_content

        except Exception as e:
            self.logger.error(f"处理日历信息时发生错误: {e}")
            return None, None

    def handle_calendar(self, response_data: dict) -> tuple:
        """
        从API响应数据中提取日历信息。

        参数:
            response_data (dict): API响应的数据字典。

        返回:
            提取到的日期和节日信息组成的元组(date, holiday)，其中：
                - date (str): 查询的日期。
                - holiday (str): 当天的节日名称。
            如果未找到或无效则返回(None, None)。
        """
        try:
            # 检查response_data是否为None或者缺少必要的键
            if not response_data or 'result' not in response_data or response_data['result'] is None:
                self.logger.error("API响应中未找到有效的日历信息")
                return None, None

            # 提取嵌套的data字典
            result = response_data['result']
            if 'data' not in result:
                self.logger.error("API响应中未找到有效的data字段")
                return None, None

            data = result['data']

            calendar_data = data.get('date')
            calendar_holiday = data.get('holiday')

            self.logger.info("获取到的日历数据: {时间: %s, 节日: %s}", calendar_data, calendar_holiday)

            if not calendar_data:
                self.logger.error("获取日历数据date为空")
            if not calendar_holiday:
                self.logger.warning("获取日历数据holiday为空")

            return calendar_data, calendar_holiday

        except Exception as e:
            self.logger.error(f"处理日历信息时发生错误: {e}")
            return None, None

    def handle_events(self):
        """
        解析并转换event_days中的日期。

        如果事件名称中包含'农历'，则将对应的农历日期转换为公历。
        如果事件名称中包含'重要'或'紧急'，则直接使用提供的日期字符串，不进行转换。
        返回一个列表，每个元素是字典，包含name和转换后的date。
        """
        parsed_events = []

        for _event in self.event_days:
            name, date_str = _event  # 更清晰地命名变量

            if '重要' in name or '紧急' in name:
                # 如果名称包含'重要'或'紧急'，则直接使用提供的日期字符串
                parsed_events.append({'name': name, 'date_str':date_str,'date': date_str})
                continue  # 跳过后续处理

            # 提取月份和日子
            month, day = map(int, date_str.replace('月', ' ').replace('日', '').split())

            if '农历' in name:
                # 将农历转换为公历
                try:
                    lunar_date = lunardate.LunarDate(self.current_year, month, day)
                    solar_date = lunar_date.toSolarDate()
                    formatted_date = f"{solar_date.year}-{solar_date.month:02d}-{solar_date.day:02d}"
                except Exception as e:
                    self.logger.error(f"转换农历日期时出错: {e}")
                    return None
            else:
                # 直接格式化日期
                formatted_date = f"{self.current_year}-{month:02d}-{day:02d}"

            # 使用字典存储name和formatted_date
            parsed_events.append({'name': name, 'date_str':date_str,'date': formatted_date})

        return parsed_events

# 示例调用
if __name__ == "__main__":
    event = EventService()
    a= event.handle_events()
    print(a)