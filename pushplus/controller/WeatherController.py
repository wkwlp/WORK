from typing import Optional
import pushplus
import random


class WeatherController:

    def __init__(self):
        self.logger = pushplus.setup_logger()
        self.weather_service = pushplus.WeatherService()

        # 初始化两个不同的服务实例
        self.services = [
            pushplus.HunYuan(model='hunyuan-pro'),
            pushplus.DeepSeek(model='deepseek-reasoner')
        ]

    def get_random_weather_condition(self, weather_info: dict) -> Optional[str]:
        """随机选择一个服务实例并获取天气状况建议"""
        service = random.choice(self.services)
        self.logger.info(f"使用服务：{service.__class__.__name__}")
        weather_condition = service.send_message(
            f'内容里包含当天和第二天的天气信息，请结合内容帮我写一段关于明日天气状况的温馨提示，要求：内容简洁（40字以内），语气温柔，生成文字不需要再编辑、开头需加上‘温馨提示：亲爱的老婆，’、内容不包含具体天气、日期、时间。内容：{weather_info}')
        if not weather_condition:
            return None

        self.logger.info(f"天气状况建议：{weather_condition}")
        return weather_condition

    def get_weather(self) -> Optional[str]:
        weather = self.weather_service.handle_weather('南宁预测天气')

        # 使用独立方法获取天气状况建议
        weather_condition = self.get_random_weather_condition(weather)

        if weather and weather_condition:
            # 注意这里的weather['day2']应该是获取第二天的天气预报，确保weather的结构符合预期
            return f'{weather.get("day2")} {weather_condition}'
        else:
            return None


if __name__ == '__main__':
    weather_controller = WeatherController()
    weather = weather_controller.get_weather()
    if weather:
        print(weather)
    else:
        print("无法获取天气信息")