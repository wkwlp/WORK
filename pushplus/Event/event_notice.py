import requests
from datetime import datetime, timedelta
from lunardate import LunarDate
import os

def get_lunar_date():
    """
    获取今天的农历月份和日期，并以 'x月x日' 的格式返回。

    :return: str, 农历月份和日期
    """
    # 获取今天的日期
    today = datetime.today()
    # 将今天的阳历日期转换为农历日期
    lunar_date = LunarDate.fromSolarDate(today.year, today.month, today.day)
    # 格式化农历日期为 'x月x日' 格式
    lunar_date_str = f"{lunar_date.month}月{lunar_date.day}日"
    return lunar_date_str


def get_birthday():
    """
    返回所有需要检查的日期信息。

    :return: list of tuples, 包含名字和日期的元组列表 [(名字, 日期), ...]
    """
    # 定义一个列表来存储不同的事件及其对应的日期
    birthdays = [
        ("妈妈农历生日", "11月16日"),
        ("爸爸农历生日", "1月27日"),
        ("老婆阳历生日", "9月29日"),
        ("弟弟农历生日", "9月16日"),
        ('和老婆在一起的纪念日', '11月14日'),
        ('外婆农历生日', '7月24日'),
        ('我的阳历生日', '10月15日'),
        ('我的农历生日', '8月29日'),
        ('重要：记得下次发朋友圈带上那张图', '10月15日')

    ]
    return birthdays

def send_reminder_email(birthdays_soon):
    """
    通过PushPlus服务发送邮件提醒。

    :param birthdays_soon: list of tuples, 包含名字、日期、阳历日期和天数的元组列表 [(名字, 日期, 阳历日期, 天数), ...]
    :return: None
    """
    # 设置本机环境系统变量，cmd
    # setx PUSHPLUS_TOKEN "token"
    # 从环境变量中获取PushPlus的服务Token
    token = os.environ.get('PUSHPLUS_TOKEN')

    # 设置PushPlus API的URL
    url = "http://www.pushplus.plus/send"

    # 构建邮件内容
    content = "未来七天有以下日子需要注意：" + "\n".join(
        [f"{name}: {date}（阳历日期：{solar_date.strftime('%Y-%m-%d')}，距离{days}天）"
         for name, date, solar_date, days in birthdays_soon])

    # 构建发送邮件所需的数据字典
    data = {
        "token": token,  # 推送使用的Token
        "title": "重要日期提醒",  # 邮件标题
        "content": content,  # 邮件内容
        "template": "txt",  # 使用的邮件模板，此处使用纯文本格式
        "channel": "mail"  # 指定推送方式为邮件
    }

    # 设置请求头，告知服务器我们将发送JSON格式的数据
    headers = {'Content-Type': 'application/json'}
    # 使用POST方法发送数据，并获取响应对象
    response = requests.post(url, json=data, headers=headers)

    # 判断请求是否成功
    if response.status_code == 200:  # 如果状态码是200，则请求成功
        print("邮件提醒发送成功")
    else:  # 如果状态码不是200，则请求失败
        print(f"邮件提醒发送失败，状态码：{response.status_code}")


def check_and_send_reminder():
    """
    检查所有预设的事件日期，并在检测到未来七天内有事件发生时发送提醒邮件。

    :return: None
    """
    # 获取所有需要检查的事件信息
    birthdays = get_birthday()
    # 获取今天的日期
    today = datetime.today()

    # 初始化一个列表来保存未来七天内的事件信息
    birthdays_soon = []

    # 遍历每个事件信息
    for name, date in birthdays:
        # 首先使用 split('月') 方法将日期字符串按照“月”进行分割
        month, day_with_ri = date.split('月')
        # 去除“日”字符
        day = day_with_ri.replace('日', '')

        # 如果是农历，转换为阳历日期
        if '农历' in name:
            # 创建农历日期对象，使用今年的年份，以及从字符串中提取的月份和日期
            lunar_date = LunarDate(today.year, int(month), int(day))
            # 将农历日期转换为阳历日期
            solar_date = lunar_date.toSolarDate()
            # 使用转换后的阳历日期创建datetime对象
            birthday_date = datetime(solar_date.year, solar_date.month, solar_date.day)
        else:
            # 直接使用阳历日期
            birthday_date = datetime(today.year, int(month), int(day))
            # 设置阳历日期
            solar_date = birthday_date

        # 计算距离事件还有多少天
        days_until_birthday = (birthday_date - today).days + 1

        # 如果事件在未来七天内
        if 0 <= days_until_birthday <= 7 or '重要' in name:
            birthdays_soon.append((name, date, solar_date, days_until_birthday))

    # 如果有未来七天内的事件，则发送邮件提醒
    if birthdays_soon:
        send_reminder_email(birthdays_soon)
    else:
        print('未来七天内未有事件')


# 主函数入口
if __name__ == "__main__":
    # 检查并发送事件提醒
    check_and_send_reminder()