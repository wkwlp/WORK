from typing import List, Optional, Dict
import send


class WeatherService:

    def __init__(self):
        self.logger = send.setup_logger()
        self.weather_api = send.WeatherApi()

    def handle_weathers(self, cities: List[str]) -> Dict[str, Optional[Dict]]:
        """
        获取并处理指定多个地区的天气信息。

        :param cities: 地区名称或查询关键词列表
        :return: 包含每个城市省份、城市及天气预报详情的字典
        """
        all_weather_info = {}
        for city in cities:
            weather_info = self._handle_single_city_weather(city)
            all_weather_info[city] = weather_info

        return all_weather_info

    def _handle_single_city_weather(self, content: str) -> Optional[Dict]:
        """
        获取并处理单个城市的天气信息。

        :param content: 地区名称或查询关键词
        :return: 包含省份、城市及天气预报详情的字典
        """
        self.logger.info(f"开始获取 {content} 的天气信息...")
        weather = self.weather_api.get_weather(content)
        self.logger.info(f"获取天气信息结果：{weather}")

        if weather.get('status') != 200:
            self.logger.error(f"获取{content}天气信息失败，错误信息：{weather.get('message')}")
            return None

        if weather['api']['forecast']:
            # 初始化空字典
            weather_dict = {}

            # 获取省份并添加到字典
            province = weather['api']['forecast'][0]['province']
            weather_dict['province'] = province

            # 获取城市并添加到字典
            city = weather['api']['forecast'][0]['city']
            weather_dict['city'] = city

            # 获取所有天气预报详情并添加到字典
            casts = weather['api']['forecast'][0]['casts']
            weather_dict['casts'] = casts

            weather_info = self._handle_weather_dict(weather_dict)
            return weather_info
        else:
            self.logger.error(f"获取 {content} 天气信息失败，请检查查询关键词是否正确。")
            return None

    @staticmethod
    def _handle_weather_dict(weather_dict: Dict) -> Dict:
        """
        提取当天和第二天的天气预报信息，并格式化为易读的字符串。

        :param weather_dict: 包含天气预报详情的字典
        :return: 包含格式化后的当天和第二天天气预报信息的字典
        """
        forecast_info = {}

        for i in range(2):  # 只处理前两天的数据
            cast = weather_dict['casts'][i]
            formatted_info = (f"日期: {cast['date']}(周{cast['week']}), "
                              f"天气: {cast['dayweather']}, 温度: {cast['nighttemp']}°C-{cast['daytemp']}°C")
            forecast_info[f'day{i + 1}'] = formatted_info

        return forecast_info


if __name__ == '__main__':
    weather_service = WeatherService()
    cities = ['南宁市预报天气', '百色市预报天气']
    weather_infos = weather_service.handle_weathers(cities)
    print(weather_infos)