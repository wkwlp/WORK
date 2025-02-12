from typing import Optional, Dict
import pushplus


class WeatherService:

    def __init__(self):
        self.logger = pushplus.setup_logger()
        self.weather_api = pushplus.WeatherApi()

    def handle_weather(self, content=None) -> Optional[Dict]:
        """
        获取并处理指定地区的天气信息。

        :param content: 地区名称或查询关键词
        :return: 包含省份、城市及天气预报详情的字典
        """
        self.logger.info("开始获取天气信息...")
        weather = self.weather_api.get_weather(content)
        self.logger.info(f"获取天气信息结果：{weather}")

        if weather.get('status') != 200:
            self.logger.error(f"获取天气信息失败，错误信息：{weather.get('message')}")
            return None

        if weather['data']['forecast']:
            # 初始化空字典
            weather_dict = {}

            # 获取省份并添加到字典
            province = weather['data']['forecast'][0]['province']
            weather_dict['province'] = province

            # 获取城市并添加到字典
            city = weather['data']['forecast'][0]['city']
            weather_dict['city'] = city

            # 获取所有天气预报详情并添加到字典
            casts = weather['data']['forecast'][0]['casts']
            weather_dict['casts'] = casts

            weather_info = self._handle_weather_dict(weather_dict)

            self.logger.info(f"获取天气预报字典成功，天气预报字典：{weather_info}")

            return weather_info
        else:
            self.logger.error("获取天气信息失败，请检查查询关键词是否正确。")
            return None
    @staticmethod
    def _handle_weather_dict(weather_dict: Dict) -> Dict:
        """
        提取当天和第二天的天气预报信息，并格式化为易读的字符串。

        :param weather_dict: 包含天气预报详情的字典
        :return: 包含格式化后的当天和第二天天气预报信息的字典
        """
        forecast_info = {}
        location = f"{weather_dict['province']}{weather_dict['city']}"
        for i in range(2):  # 只处理前两天的数据
            cast = weather_dict['casts'][i]
            formatted_info = (f"{location}-天气预报：日期: {cast['date']}(周{cast['week']}), "
                              f"天气: {cast['dayweather']}, 温度: {cast['nighttemp']}°C-{cast['daytemp']}°C")
            forecast_info[f'day{i + 1}'] = formatted_info

        return forecast_info


if __name__ == '__main__':
    weather_service = WeatherService()
    a = weather_service.handle_weather('南宁市预报天气')
    print(a)
