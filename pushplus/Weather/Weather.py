import requests
import os
from datetime import datetime, timedelta


class WeatherInfoFetcher:
    """
    获取和处理天气信息的类。

    Attributes:
        amap_key (str): 高德地图API密钥。
    """

    def __init__(self):
        """
        初始化WeatherInfoFetcher实例，从环境变量中读取高德地图API密钥。
        """
        self.amap_key = os.environ.get('AMAP_KEY')

    @staticmethod
    def get_tomorrow_date():
        """
        获取明天的日期，并将其格式化为 'YYYY-MM-DD' 的形式。

        Returns:
            str: 明天的日期，格式为 'YYYY-MM-DD' 的字符串。
        """
        # 获取今天的日期和时间
        today = datetime.now()
        # 通过向今天的日期添加一天来计算明天的日期
        tomorrow = today + timedelta(days=1)
        # 使用 strftime 方法将明天的日期格式化为 'YYYY-MM-DD' 的字符串格式
        formatted_tomorrow = tomorrow.strftime('%Y-%m-%d')
        # 返回格式化后的明天的日期
        return formatted_tomorrow

    def construct_weather_url(self, city="450103", extensions="all", output="json"):
        """
        构造高德地图天气API的请求URL。

        Args:
            city (str): 城市编码，默认为南宁市青秀区（450103）。
            extensions (str): 扩展信息类型，默认为'all'（返回预报天气），可选'base'（返回实况天气）。
            output (str): 返回格式，默认为'json'，可选'xml'。

        Returns:
            str: 构造好的完整请求URL。
        """
        base_url = "https://restapi.amap.com/v3/weather/weatherInfo"
        complete_url = f"{base_url}?city={city}&key={self.amap_key}&extensions={extensions}&output={output}"
        return complete_url

    def handle_weather_data(self, data, tomorrow_date):
        """
        处理天气数据并打印相关信息。

        Args:
            data (dict): API响应的JSON数据。
            tomorrow_date (str): 明天的日期。

        Returns:
            tuple: 包含天气预报信息的字符串和天气状况字符串的元组。
        """
        # 检查API请求的状态码是否为成功状态
        if data.get('status') != '1':
            print("请求 API 失败:", data.get('infocode'), data.get('info'))
            return None, None
        # 从API响应数据中提取预报数据
        forecasts = data.get('forecasts')
        if not forecasts:
            print("没有找到天气信息。")
            return None, None
        # 从预报数据中提取具体的天气预报列表
        forecast_list = forecasts[0].get('casts', [])

        # 调用 get_weather_forecast 函数处理预报数据并获取天气预报信息字符串
        weather_forecast, weather_condition = self.get_weather_forecast(forecast_list, tomorrow_date)
        return weather_forecast, weather_condition

    def get_weather_forecast(self, forecast_list, tomorrow_date):
        """
        返回明天的天气预报信息作为字符串，并附带天气状况。

        Args:
            forecast_list (list): 预报数据列表。
            tomorrow_date (str): 明天的日期。

        Returns:
            tuple: 包含预报信息字符串和天气状况字符串的元组。
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

    def get_weather_live(self, realtime_weather):
        """
        返回实时天气信息作为字符串。

        Args:
            realtime_weather (dict): 实时天气信息的字典。

        Returns:
            str: 包含实时天气信息的字符串。
        """
        # 初始化一个空字符串用于存储实时天气信息
        result = ""
        # 如果实时天气信息存在且非空
        if realtime_weather:
            # 添加城市名和实时天气信息标题
            result += f"南宁市{realtime_weather['city']}-实时天气信息:\n"

            # 添加天气状况信息
            result += f"天气状况: {realtime_weather['weather']}\n"

            # 添加当前温度信息
            result += f"温度: {realtime_weather['temperature']}°C\n"
        # 返回构造好的天气信息字符串
        return result

    def fetch_weather_info(self, extension_type='all'):
        """
        获取预报天气信息。

        Args:
            extension_type (str): 'all'获取预报天气，'base'获取实时天气。

        Returns:
            tuple: 包含天气预报信息的字符串或None（如果请求失败）。
        """
        # 获取完整的URL
        complete_url = self.construct_weather_url(extensions=extension_type)


        try:
            # 发送 GET 请求并获取响应
            response = requests.get(complete_url)
            # 检查 HTTP 响应状态码，如果状态码不是200，则抛出异常
            response.raise_for_status()
            # 将 JSON 响应转换为 Python 字典
            data = response.json()
            # 获取明天的日期
            tomorrow_date = self.get_tomorrow_date()
            # 处理数据，获取天气预报信息
            weather_forecast, weather_condition = self.handle_weather_data(data, tomorrow_date)
            # 返回天气预报信息
            return weather_forecast, weather_condition

        except requests.exceptions.RequestException as e:
            print(f"请求过程中发生错误: {e}")
            return None, None

    def fetch_live_weather_info(self):
        """
        获取实时天气信息。

        Returns:
            str: 实时天气信息的字符串或None（如果请求失败）。
        """
        complete_url = self.construct_weather_url(extensions='base')
        try:
            response = requests.get(complete_url)
            response.raise_for_status()
            data = response.json()
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
            weather_live = self.get_weather_live(live_weather)

            return weather_live
        except requests.exceptions.RequestException as e:
            print(f"请求过程中发生错误: {e}")
            return None

    def get_weather_advice(self, weather_condition):
        """
        根据天气状况给出温馨提示。

        Args:
            weather_condition (str): 天气状况描述。

        Returns:
            str: 温馨提示字符串。
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


class WeatherReminderSender:
    """
    通过PushPlus服务发送邮件提醒的类。

    Attributes:
        pushplus_token (str): PushPlus的服务Token。
    """

    def __init__(self):
        """
        初始化WeatherReminderSender实例，从环境变量中读取PushPlus的服务Token。
        """
        self.pushplus_token = os.environ.get('PUSHPLUS_TOKEN')

    def send_reminder_email(self, title, content):
        """
        通过PushPlus服务发送邮件提醒。

        Args:
            title (str): 邮件标题。
            content (str): 邮件内容。
        """
        url = "http://www.pushplus.plus/send"
        # 构建发送邮件所需的数据字典
        data = {
            "token": self.pushplus_token,  # 推送使用的Token
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
        if response.status_code == 200:
            print("邮件提醒发送成功")
        else:
            print(f"邮件提醒发送失败，状态码：{response.status_code}")


def main():
    """
    主程序入口，用于获取天气信息并发送邮件提醒。
    """
    # 创建天气信息获取器实例
    weather_fetcher = WeatherInfoFetcher()
    # 创建邮件发送器实例
    email_sender = WeatherReminderSender()

    # 获取实时天气信息
    realtime_weather = weather_fetcher.fetch_live_weather_info()
    # 获取预报天气信息
    forecast_weather, weather_condition = weather_fetcher.fetch_weather_info()
    # 获取天气建议
    weather_condition = weather_fetcher.get_weather_advice(weather_condition)

    # 拼接天气信息
    weather = f'{realtime_weather}{forecast_weather}{weather_condition}'
    # 发送邮件提醒
    email_sender.send_reminder_email('天气提醒', weather)


if __name__ == "__main__":
    main()