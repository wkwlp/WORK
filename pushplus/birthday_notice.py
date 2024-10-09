import requests
from datetime import datetime
from lunardate import LunarDate


def get_lunar_date():
    """
    获取今天的农历月份和日期，并以 'x月x日' 的格式返回。

    :return: str, 农历月份和日期
    """
    # 获取今天的日期
    today = datetime.today()

    # 将公历日期转换为农历日期
    lunar_date = LunarDate.fromSolarDate(today.year, today.month, today.day)

    # 格式化农历月份和日期
    lunar_date = f"{lunar_date.month}月{lunar_date.day}日"

    return lunar_date


def send_reminder_email(birthdays_today):
    """
    通过PushPlus服务发送邮件提醒。

    :param birthdays_today: list of tuples, 包含名字和日期的元组列表 [(名字, 日期), ...]
    :return: None
    """
    # 设置PushPlus的服务Token
    token = "30db2b55c89c450cb5377d35cc8b098b"

    # 设置PushPlus API的URL
    url = "http://www.pushplus.plus/send"

    # 构建邮件内容
    content = "今天有以下生日需要祝贺：" + "\n".join([f"{name}: {date}" for name, date in birthdays_today])

    # 构建发送邮件所需的数据字典
    data = {
        "token": token,  # 推送使用的Token
        "title": "生日提醒",  # 邮件标题
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


def get_birthday():
    """
    返回所有需要检查的生日信息。

    :return: list of tuples, 包含名字和日期的元组列表 [(名字, 日期), ...]
    """
    # 定义一个列表来存储不同的生日及其对应的日期
    birthdays = [
        ("妈妈农历生日", "11月16日"),
        ("爸爸农历生日", "1月27日"),
        ("老婆阳历生日", "10月10日"),
        ("弟弟农历生日", "9月7日")
    ]

    return birthdays


def check_and_send_reminder():
    """
    检查所有预设的生日日期，并在检测到今天是某个生日时发送提醒邮件。

    :return: None
    """
    # 获取所有需要检查的生日信息
    birthdays = get_birthday()

    # 获取今天的农历月份和日期
    lunar_date = get_lunar_date()

    # 获取今天的日期
    today = datetime.today()

    # 格式化今天的日期
    now_date = f"{today.month}月{today.day}日"

    # 初始化一个列表来保存今天过生日的人的信息
    birthdays_today = []

    # 遍历每个生日信息
    for name, date in birthdays:
        # 如果是农历生日，并且今天是这个人的农历生日
        if '农历' in name and date == lunar_date:
            birthdays_today.append((name, date))
        # 如果是阳历生日，并且今天是这个人的阳历生日
        elif not '农历' in name and date == now_date:
            birthdays_today.append((name, date))

    # 如果今天有人过生日，则发送邮件提醒
    if birthdays_today:
        send_reminder_email(birthdays_today)
    else:
        print('今天未有人生日')


# 主函数
if __name__ == "__main__":
    # 检查并发送生日提醒
    check_and_send_reminder()