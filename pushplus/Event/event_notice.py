import requests
from datetime import datetime, timedelta
from lunardate import LunarDate
import os


class DateHandler:
    """
    用于处理日期相关的任务，如计算农历和阳历日期等。

    属性:
        today (datetime.datetime): 当前日期。
    """

    def __init__(self):
        """
        初始化日期处理器，设置今天日期。
        """
        self.today = datetime.today()

    def get_lunar_date(self):
        """
        获取今天的农历月份和日期，并以 'x月x日' 的格式返回。

        :return: str, 农历月份和日期
        """
        # 将今天的阳历日期转换为农历日期
        lunar_date = LunarDate.fromSolarDate(self.today.year, self.today.month, self.today.day)
        # 格式化农历日期为 'x月x日' 格式
        return f"{lunar_date.month}月{lunar_date.day}日"

    def get_event_days(self):
        """
        返回所有需要检查的日期信息。

        :return: list of tuples, 包含名字和日期的元组列表 [(名字, 日期), ...]
        """
        # 定义一个列表来存储不同的事件及其对应的日期
        event_days = [
            ("妈妈农历生日", "11月16日"),
            ("爸爸农历生日", "1月27日"),
            ("老婆阳历生日", "9月29日"),
            ('和老婆在一起的纪念日', '11月14日'),
            ('外婆农历生日', '7月24日'),
            ('我的阳历生日', '10月15日'),
            ('我的农历生日', '8月29日'),
            ('重要：记得下次发朋友圈带上那张图', '10月15日')
        ]
        return event_days

    def calculate_days_until_event(self, name, date):
        """
        计算指定事件距离今天的天数。

        :param name: str, 事件名称
        :param date: str, 事件日期
        :return: tuple, 包含事件名称、日期、阳历日期和天数的元组
        """
        # 分割日期字符串以获取月份和日期
        month, day_with_ri = date.split('月')
        day = day_with_ri.replace('日', '')

        # 如果是农历日期，则将其转换为阳历日期
        if '农历' in name:
            lunar_date = LunarDate(self.today.year, int(month), int(day))
            solar_date = lunar_date.toSolarDate()
            # 使用转换后的阳历日期创建datetime对象
            event_datetime = datetime(solar_date.year, solar_date.month, solar_date.day)
        else:
            # 直接使用阳历日期
            event_datetime = datetime(self.today.year, int(month), int(day))

        # 计算距离事件还有多少天
        days_until = (event_datetime - self.today).days + 1
        return name, date, event_datetime, days_until


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

        初始化时会从环境变量中获取PUSHPLUS_TOKEN。
        如果环境变量未设置，将抛出一个ValueError异常。
        """
        self.token = os.getenv('PUSHPLUS_TOKEN')
        if not self.token:
            raise ValueError("PUSHPLUS_TOKEN 环境变量必须设置。")
        self.url = "http://www.pushplus.plus/send"

    def send_reminder(self, title,event_days_soon):
        """
        通过PushPlus服务发送邮件提醒。

        :param event_days_soon: list of tuples, 包含事件名称、日期、阳历日期和天数的元组列表
        """
        # 构建邮件内容
        content = "未来有以下日子需要注意：" + "\n".join(
            [f"{name}: {date}（阳历日期：{solar_date.strftime('%Y-%m-%d')}，距离{days}天）"
             for name, date, solar_date, days in event_days_soon])

        # 构建发送邮件所需的数据字典
        data = {
            "token": self.token,    # 推送使用的Token
            "title": title,  # 邮件标题
            "content": content,    # 邮件内容
            # "topic": "wkwlp",  # 群组编码
            "template": "txt",  # 使用的邮件模板，此处使用纯文本格式
            "channel": "mail"   # 指定推送方式为邮件
        }

        # 设置请求头，告知服务器我们将发送JSON格式的数据
        headers = {'Content-Type': 'application/json'}

        # 使用POST方法发送数据，并获取响应对象
        try:
            response = requests.post(self.url, json=data, headers=headers)
            # 判断请求是否成功
            if response.status_code == 200:
                print("邮件提醒发送成功")
            else:
                print(f"邮件提醒发送失败，状态码：{response.status_code}")
        except Exception as e:
            print(f"邮件发送时发生错误：{e}")


def main():
    """
    检查所有预设的事件日期，并在检测到未来七天内有事件发生时发送提醒邮件。
    """
    try:
        date_handler = DateHandler()  # 创建日期处理器实例
        email_notifier = EmailNotifier()  # 创建邮件通知器实例

        # 获取所有需要检查的事件信息
        event_days = date_handler.get_event_days()

        # 初始化一个列表来保存未来七天内的事件信息
        event_days_soon = []

        # 遍历每个事件信息
        for name, date in event_days:
            event_info = date_handler.calculate_days_until_event(name, date)
            name, date, solar_date, days_until = event_info

            # 如果事件在未来七天内或标记为重要，则添加到列表
            if 0 <= days_until <= 7 or '重要' in name:
                event_days_soon.append(event_info)
                print(f"{name} 在未来七天内，剩余天数：{days_until}")

        # 如果有未来七天内的事件，则发送邮件提醒
        if event_days_soon:
            print("正在发送邮件提醒...")
            email_notifier.send_reminder('重要日期提醒', event_days_soon)
        else:
            print('未来七天内未有事件')
    except Exception as e:
        print(f"检查和发送提醒时发生错误：{e}")


# 主函数入口
if __name__ == "__main__":
    # 检查并发送事件提醒
    main()