import os
import json
from configparser import ConfigParser, NoSectionError, NoOptionError

# 设置日志记录
from pushplus.config.logger_config import setup_logger


class ConfigReader:

    def __init__(self, config_path=None):
        # 初始化日志记录器
        self.logger = setup_logger()

        # 加载配置文件
        self._load_config(config_path)

    def _load_config(self, config_path=None):
        """加载配置文件"""
        # 默认寻找当前目录下的config.ini文件
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), 'config.ini')

        if not os.path.exists(config_path):
            self.logger.error(f"未找到配置文件: {config_path}")
            raise FileNotFoundError(f"无法在 {config_path} 找到配置文件")

        self.config = ConfigParser()
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                self.config.read_file(file)
        except IOError as e:
            self.logger.error(f"读取配置文件失败: {e}")
            raise

    def get_love_quote_config(self) -> dict:
        try:
            love_quote_section = self.config['LoveQuoteConfig']
            raw_config = {
                'SayLoveURL': love_quote_section.get('SayLoveURL'),
                'CaiHongPiURL': love_quote_section.get('CaiHongPiURL'),
                'Custom_Values': json.loads(love_quote_section.get('Custom_Values')),
                'Max_Retries': love_quote_section.getint('Max_Retries')
            }
            return raw_config
        except (NoSectionError, NoOptionError) as e:
            self.logger.error(f"读取 LoveQuoteConfig 配置失败: {e}")
            return {}

    def get_send_email_config(self) -> dict:
        try:
            send_email_section = self.config['SendEmailConfig']
            send_email_config = {
                'URL': send_email_section.get('URL'),
                'Template': send_email_section.get('Template'),
                'Channel': send_email_section.get('Channel')
            }
            return send_email_config
        except (NoSectionError, NoOptionError) as e:
            self.logger.error(f"读取 SendEmailConfig 配置失败: {e}")
            return {}

    def get_event_config(self) -> dict:
        try:
            event_section = self.config['EventConfig']
            raw_config = {
                'CalendarURL': event_section.get('CalendarURL'),
                'EventDays': json.loads(event_section.get('EventDays')),
                'Day': event_section.getint('Day'),
                'Name': json.loads(event_section.get('Name'))
            }
            return raw_config
        except (NoSectionError, NoOptionError) as e:
            self.logger.error(f"读取 EventConfig 配置失败: {e}")
            return {}

    def get_weather_config(self) -> dict:
        try:
            weather_section = self.config['WeatherConfig']
            weather_config = {
                'URL': weather_section.get('URL'),
                'Output': json.loads(weather_section.get('Output')),
                'City': json.loads(weather_section.get('City')),
                'Extension': json.loads(weather_section.get('Extensions'))
            }
            return weather_config
        except (NoSectionError, NoOptionError) as e:
            self.logger.error(f"读取 WeatherConfig 配置失败: {e}")
            return {}

    def get_deep_seek_config(self) -> dict:
        try:
            deep_seek_section = self.config['DeepSeekConfig']
            deep_seek_config = {
                'URL': deep_seek_section.get('URL')
            }
            return deep_seek_config
        except (NoSectionError, NoOptionError) as e:
            self.logger.error(f"读取 DeepSeekConfig 配置失败: {e}")
            return {}

    def get_hunyuan_config(self) -> dict:
        try:
            hunyuan_lite_section = self.config['HunYuanConfig']
            hunyuan_lite_config = {
                'URL': hunyuan_lite_section.get('URL')
            }
            return hunyuan_lite_config
        except (NoSectionError, NoOptionError) as e:
            self.logger.error(f"读取 HunYuanConfig 配置失败: {e}")
            return {}


# 使用方法：
if __name__ == '__main__':
    try:
        reader = ConfigReader()
        print(reader.get_love_quote_config())
        print(reader.get_send_email_config())
        print(reader.get_event_config())
        print(reader.get_weather_config())
        print(reader.get_hunyuan_config())
    except Exception as e:
        print(f"程序运行出错: {e}")