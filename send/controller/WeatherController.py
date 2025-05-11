from typing import Optional, Dict, Any
import send
import random


class WeatherController:

    def __init__(self):
        self.logger = send.setup_logger()
        config = send.ConfigReader()
        self.condition = config.get_weather_config().get('Condition')
        self.cities = config.get_weather_config().get('Cities')
        self.weather_service = send.WeatherService()

        # 初始化两个不同的服务实例
        self.services = {
            'hunyuan': send.HunYuan(model='hunyuan-pro'),
            'deepseek': send.DeepSeek(model='deepseek-reasoner')
        }

    def _get_weather_condition(self, weather_info: Dict[str, Any], service_name: Optional[str] = None) -> Optional[str]:
        """根据service_name指定或随机选择一个服务实例并获取天气状况建议"""
        if service_name and service_name in self.services:
            service = self.services[service_name]
            self.logger.info(f"手动选择的服务：{service.__class__.__name__}")
        else:
            service = random.choice(list(self.services.values()))
            self.logger.info(f"随机选择的服务：{service.__class__.__name__}")

        # 将所有城市的天气信息转换为字符串格式
        weather_str = ', '.join([f"{city}: {info['day2']}" for city, info in weather_info.items()])

        weather_condition = service.send_message(
            f'{weather_str} {self.condition}'
        )
        if not weather_condition:
            self.logger.warning(f"{service.__class__.__name__}服务返回空结果")
            return None

        self.logger.info(f"天气状况建议：{weather_condition}")
        return weather_condition

    def get_weather(self, service_name: Optional[str] = None) -> Optional[str]:
        """获取天气信息并返回天气状况建议"""
        weather = self.weather_service.handle_weathers(self.cities)
        self.logger.info(f"天气信息：{weather}")

        # 获取天气状况建议
        weather_condition = self._get_weather_condition(weather, service_name='deepseek')

        if weather_condition is None:
            weather_condition = "温馨提示：今日接口有问题，老婆注意安全，顺便跟我说一下~"

        # 拼接天气信息和天气状况建议
        if weather:
            # 构建最终的天气信息字符串
            weather_summary = []
            for city, info in weather.items():
                day2_info = info.get('day2', '代码有问题，无数据')
                weather_summary.append(f"{city}: {day2_info}")

            return f"{'; '.join(weather_summary)} {weather_condition}"
        else:
            return None


if __name__ == '__main__':
    weather_controller = WeatherController()

    # 示例：可以传入'service_name'参数来手动选择服务，或者不传参以随机选择
    weather = weather_controller.get_weather(service_name='hunyuan')  # 手动选择
    # 或者
    # weather = weather_controller.get_weather()  # 默认随机选择

    if weather:
        print(weather)
    else:
        print("无法获取天气信息")
