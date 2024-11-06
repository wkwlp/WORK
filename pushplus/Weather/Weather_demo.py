import requests
import os
from datetime import datetime, timedelta


def get_tomorrow_date():
    """
    获取明天的日期，并将其格式化为 'YYYY-MM-DD' 的形式。

    :return: 明天的日期，格式为 'YYYY-MM-DD' 的字符串。
    """
    # 获取今天的日期和时间
    today = datetime.now()

    # 通过向今天的日期添加一天来计算明天的日期
    tomorrow = today + timedelta(days=1)

    # 使用 strftime 方法将明天的日期格式化为 'YYYY-MM-DD' 的字符串格式
    formatted_tomorrow = tomorrow.strftime('%Y-%m-%d')

    # 返回格式化后的明天的日期
    return formatted_tomorrow


def weather_url(AMAP_KEY, city="450103", extensions="all", output="json"):
    """
    构造高德地图天气API的请求URL。

    :param AMAP_KEY: str, 高德地图API的密钥。
    :param city: str, 城市编码，默认为南宁市青秀区（450103）。
    :param extensions: str, 扩展信息类型，默认为'all'（返回预报天气），可选'base'（返回实况天气）。
    :param output: str, 返回格式，默认为'json'，可选'xml'。
    :return: str, 构造好的完整请求URL。
    """
    # 构造基本URL
    base_url = "https://restapi.amap.com/v3/weather/weatherInfo"

    # 构造完整的请求URL
    complete_url = f"{base_url}?city={city}&key={AMAP_KEY}&extensions={extensions}&output={output}"

    return complete_url




def handle_weather_data(data, tomorrow_date):
    """
    处理天气数据并打印相关信息。

    :param data: API响应的JSON数据
    :param tomorrow_date: 明天的日期
    :return weather_forecast: 包含天气预报信息的字符串
    """
    # 检查API请求的状态码是否为成功状态
    if data.get('status') != '1':
        # 如果状态码不是'1'，则认为请求失败，并打印错误信息
        print("请求 API 失败:", data.get('infocode'), data.get('info'))
        return

    # 从API响应数据中提取预报数据
    forecasts = data.get('forecasts')
    if not forecasts:
        # 如果没有找到预报数据，则打印提示信息
        print("没有找到天气信息。")
        return

    # 从预报数据中提取具体的天气预报列表
    forecast_list = forecasts[0].get('casts', [])

    # 调用 get_weather_forecast 函数处理预报数据并获取天气预报信息字符串
    weather_forecast,weather_condition = get_weather_forecast(forecast_list, tomorrow_date)

    # 返回天气预报信息字符串
    return weather_forecast,weather_condition

def get_weather_forecast(forecast_list, tomorrow_date):
    """
    返回明天的天气预报信息作为字符串，并附带天气状况。

    :param forecast_list: 预报数据列表，每个元素是一个字典，包含如下键：
                          'date': 日期,
                          'week': 星期几,
                          'dayweather': 白天天气状况,
                          'daytemp': 白天最高温度,
                          'nighttemp': 夜间最低温度
    :param tomorrow_date: 明天的日期，格式为 'YYYY-MM-DD'
    :return: 一个元组，包含两个元素：预报信息字符串和天气状况字符串
    """
    # 初始化一个空字符串用于存储最终的预报信息
    result = "南宁市青秀区-预报天气信息:\n"

    # 初始化天气状况为默认值
    weather_condition = '未知天气状况'

    # 标记是否找到了明天的天气预报信息，默认为False
    found = False

    # 遍历预报数据列表
    for forecast in forecast_list:
        # 获取当前预报记录的日期
        forecast_date = forecast['date']

        # 如果找到了匹配的日期（即明天的日期）
        if forecast_date == tomorrow_date:
            # 将日期信息添加到结果字符串中
            result += f"日期: {forecast_date}(周{forecast['week']})\n"

            # 将白天的天气状况添加到结果字符串中
            result += f"白天天气状况: {forecast['dayweather']}\n"

            # 将白天和夜间温度范围添加到结果字符串中
            result += f"温度: {forecast['nighttemp']}°C-{forecast['daytemp']}°C\n"

            # 更新天气状况
            weather_condition = forecast['dayweather']

            # 设置标记为True表示已经找到了对应的天气预报
            found = True

            # 结束循环，不再查找其他记录
            break

    # 如果没有找到对应的天气预报，则在结果字符串中加入提示信息
    if not found:
        result += "未找到明天的天气信息。"

    # 返回预报信息字符串和天气状况字符串的元组
    return result, weather_condition


def get_weather_live(realtime_weather):
    """
    返回实时天气信息作为字符串。

    :param realtime_weather: 实时天气信息的字典，应包含以下键：
                             'city': 城市名称,
                             'weather': 当前天气状况,
                             'temperature': 当前温度
    :return: 包含实时天气信息的字符串
    """
    # 初始化一个空字符串用于存储实时天气信息
    result = ""

    # 如果实时天气信息存在且非空
    if realtime_weather:
        # 构造天气信息字符串
        # 添加城市名和实时天气信息标题
        result += f"南宁市{realtime_weather['city']}-实时天气信息:\n"

        # 添加天气状况信息
        result += f"天气状况: {realtime_weather['weather']}\n"

        # 添加当前温度信息
        result += f"温度: {realtime_weather['temperature']}°C\n"

    # 返回构造好的天气信息字符串
    return result



def get_all_weather(AMAP_KEY):
    """
    获取预报天气信息。

    :param AMAP_KEY: 高德地图API密钥
    :return: 包含天气预报信息的字符串或None（如果请求失败）
    """
    # 获取完整的URL
    complete_url = weather_url(AMAP_KEY)  # 假设 `weather_url` 已经定义好，能够构造出正确的API URL

    try:
        # 发送 GET 请求并获取响应
        response = requests.get(complete_url)

        # 检查 HTTP 响应状态码，如果状态码不是200，则抛出异常
        response.raise_for_status()

        # 将 JSON 响应转换为 Python 字典
        data = response.json()

        # 获取明天的日期
        tomorrow_date = get_tomorrow_date()  # 假设 `get_tomorrow_date` 已经定义好，能够返回明天的日期

        # 处理数据，获取天气预报信息
        weather_forecast,weather_condition = handle_weather_data(data, tomorrow_date)

        # 返回天气预报信息
        return weather_forecast,weather_condition

    except requests.exceptions.RequestException as e:
        # 如果在请求过程中出现异常，则打印错误信息
        print(f"请求过程中发生错误: {e}")
        # 返回 None 表示请求失败
        return None


def get_base_weather(amap_key):
    """
    获取实时天气信息。

    :param amap_key: 高德地图API密钥
    :return: 实时天气信息的字典或None（如果请求失败或没有找到实时天气信息）
    """
    # 构造实时天气信息的URL
    complete_url = weather_url(amap_key, extensions='base')

    try:
        # 发送 GET 请求并获取响应
        response = requests.get(complete_url)

        # 检查 HTTP 响应状态码，如果状态码不是200，则抛出异常
        response.raise_for_status()

        # 将 JSON 响应转换为 Python 字典
        data = response.json()

        # 检查请求是否成功
        if data.get('status') != '1':
            print("请求 API 失败:", data.get('infocode'), data.get('info'))
            return None

        # 获取实时天气数据
        lives = data.get('lives')
        if not lives:
            print("没有找到实时天气信息。")
            return None

        # 提取实时天气信息
        live_weather = lives[0]

        # 获取实时天气信息字符串
        weather_live = get_weather_live(live_weather)

        # # 打印实时天气信息
        # print(weather_live)

        # 返回实时天气信息字符串
        return weather_live

    except requests.exceptions.RequestException as e:
        # 如果在请求过程中出现异常，则打印错误信息并返回None
        print(f"请求过程中发生错误: {e}")
        return None


def get_weather_advice(weather_condition):
    """
    根据天气状况给出温馨提示。

    :param weather_condition: 天气状况描述
    :return: 温馨提示字符串
    """
    advices = {
        '晴': '明日天气温馨提示：亲爱的老婆，明天阳光明媚，适合户外活动，别忘了涂抹防晒霜哦！',
        '晴朗': '明日天气温馨提示：亲爱的老婆，明天阳光明媚，适合户外活动，别忘了涂抹防晒霜哦！',
        '多云': '明日天气温馨提示：亲爱的老婆，明天天气多云，温度适宜，也要小心紫外线哦~',
        '阴': '明日天气温馨提示：亲爱的老婆，明天天空有些阴沉，记得带把伞以防突然下雨。',
        '小雨': '明日天气温馨提示：亲爱的老婆，明天有小雨，请带上雨具，注意保暖，小心路滑。',
        '中雨': '明日天气温馨提示：亲爱的老婆，明天中等强度的降雨可能会造成路面湿滑，请减速慢行，并保持安全距离。',
        '大雨': '明日天气温馨提示：亲爱的老婆，明天有大雨，尽量减少外出，出行请注意安全，避免积水路段。',
        '暴雨': '明日天气温馨提示：亲爱的老婆，明天暴雨来袭，请留在室内，远离窗户，确保安全。',
        '阵雨': '明日天气温馨提示：亲爱的老婆，明天阵雨时有时无，请随身携带雨具，以免突然降雨。',
        '雷阵雨': '明日天气温馨提示：亲爱的老婆，明天雷阵雨可能伴有雷电，请注意避雷，避免在树下躲雨。',
        '雨夹雪': '明日天气温馨提示：亲爱的老婆，明天雨夹雪天气，路面可能湿滑，驾车出行请注意安全。',
        '小雪': '明日天气温馨提示：亲爱的老婆，明天小雪天气，记得穿上保暖衣物，欣赏雪景的同时注意防寒。',
        '中雪': '明日天气温馨提示：亲爱的老婆，明天中雪天气，道路可能会积雪，请穿戴防滑鞋具，谨慎出行。',
        '大雪': '明日天气温馨提示：亲爱的老婆，明天有大雪，请尽量减少外出，若必须外出，请穿戴保暖并做好防滑措施。',
        '暴雪': '明日天气温馨提示：亲爱的老婆，明天暴雪天气非常危险，请留在室内，确保家中有足够食物及生活用品。',
        '雾': '明日天气温馨提示：亲爱的老婆，明天雾天能见度低，请驾驶员开启雾灯，谨慎驾驶；雾霾天气，请佩戴口罩，减少户外活动。',
        '雾霾': '明日天气温馨提示：亲爱的老婆，明天雾天能见度低，请驾驶员开启雾灯，谨慎驾驶；雾霾天气，请佩戴口罩，减少户外活动。',
        '霾': '明日天气温馨提示：亲爱的老婆，明天霾天气质污染严重，请尽量减少外出，外出时佩戴口罩。',
        '沙尘暴': '明日天气温馨提示：亲爱的老婆，明天沙尘暴天气，请关闭门窗，尽量留在室内，外出请戴口罩和护目镜。',
        '强对流': '明日天气温馨提示：亲爱的老婆，明天强对流天气可能导致突发性天气变化，请随时关注气象预警信息。',
        '冰雹': '明日天气温馨提示：亲爱的老婆，预计明天会有冰雹，请保护好车辆，尽量避免外出，以免受伤。'
    }
    return advices.get(weather_condition, '明日天气温馨提示：亲爱的老婆，高德地图返回的内容不在代码范围内！')

def send_reminder_email(title,content):
    """
    通过PushPlus服务发送邮件提醒。

    :param content:
    :return: None
    """
    # 设置本机环境系统变量，cmd
    # setx PUSHPLUS_TOKEN "token"
    # 从环境变量中获取PushPlus的服务Token
    token = os.environ.get('PUSHPLUS_TOKEN')

    # 设置PushPlus API的URL
    url = "http://www.pushplus.plus/send"


    # 构建发送邮件所需的数据字典
    data = {
        "token": token,  # 推送使用的Token
        "title": title,  # 邮件标题
        "content": content,  # 邮件内容
        # "topic": "wkwlp",  # 群组编码
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


if __name__ == "__main__":
    # 使用高德地图 API 密钥
    # 设置本机环境系统变量，cmd
    # setx AMAP_KEY "token"
    # 从环境变量中获取高德地图API的Token
    AMAP_KEY = os.environ.get('AMAP_KEY')

    # 获取实时天气信息
    realtime_weather = get_base_weather(AMAP_KEY)

    # 获取预报天气信息
    forecast_weather,weather_condition = get_all_weather(AMAP_KEY)

    weather_condition =get_weather_advice(weather_condition)
    blank = '                                '
    # 将实时天气和预报天气信息拼接起来
    weather = f'{realtime_weather}{forecast_weather}{weather_condition}'

    send_reminder_email('天气提醒',weather)
    # # 最终只打印一次拼接后的结果
    # print(weather)

