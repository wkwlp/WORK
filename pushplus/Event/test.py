# import requests
# from datetime import datetime, timedelta
# import os
#
#
# class CalendarAPI:
#     """
#     用于调用日历API的类，提供获取指定日期的日历详情功能。
#     """
#
#     def __init__(self, api_key):
#         """
#         初始化CalendarAPI实例。
#
#         :param api_key: API访问密钥
#         """
#         self.api_url = 'http://v.juhe.cn/calendar/day'  # 日历API的URL
#         self.api_key = api_key  # 用户的API密钥
#
#     @staticmethod
#     def format_date(date):
#         """
#         将日期格式化为 YYYY-M-D 格式，并移除月份和日期小于10时的前导0。
#
#         :param date: datetime对象，表示需要格式化的日期
#         :return: 格式化后的字符串形式的日期
#         """
#         formatted_date = date.strftime('%Y-%m-%d')
#         # 移除月份和日期小于10时的前导0
#         return formatted_date.replace('-0', '-')
#
#     def get_calendar_info(self, date=None):
#         """
#         获取指定日期的日历信息。
#
#         :param date: datetime对象，默认为None，如果未提供则使用当前日期
#         :return: 包含请求结果的字典
#         """
#         if date is None:
#             # 如果没有提供日期，则使用明天的日期
#             date_tomorrow = datetime.today() + timedelta(days=1)
#             print(f"date_tomorrow:{date_tomorrow}")
#             # 格式化日期
#             date = self.format_date(date_tomorrow)
#
#         # 构造请求参数
#         request_params = {
#             'key': self.api_key,
#             'date': date,
#         }
#
#         try:
#             # 发送GET请求
#             response = requests.get(self.api_url, params=request_params)
#             response.raise_for_status()  # 检查请求是否成功
#         except requests.RequestException as e:
#             # 处理请求异常
#             print(f"请求失败: {e}")
#             return {'error': str(e)}
#
#         data = response.json()
#         # 获取对应值，如果不存在则返回空字典{}
#         result = data.get('result', {}).get('data', {})
#         holiday = result.get('holiday')
#         date = result.get('date')
#
#         # 拼接return值
#         str = f'{date}：{holiday}'
#         # 解析并返回响应结果
#         return str
#
# # 使用示例
# if __name__ == "__main__":
#     # 用户的API密钥
#     api_key = os.environ.get('CalendarAPI_KEY')
#     calendar_api = CalendarAPI(api_key)
#
#     # 获取今天的日历信息
#
#     result = calendar_api.get_calendar_info('2024-11-7')
#
#
#     print(result)