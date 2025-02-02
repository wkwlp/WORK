import os
import json
from configparser import ConfigParser, NoSectionError, NoOptionError

# 设置日志记录
from pushplus.config.logger_config import setup_logger


class ConfigReader:

    def __init__(self, config_path=None):
        # 初始化日志记录器
        self.logger = setup_logger()

        # 默认寻找当前目录下的config.ini文件
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), 'config.ini')

        if not os.path.exists(config_path):
            self.logger.error(f"未找到配置文件: {config_path}")
            raise FileNotFoundError(f"无法在 {config_path} 找到配置文件")

        self.config = ConfigParser()
        self.json = json  # 将 json 模块赋值给实例变量

        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                self.config.read_file(file)
        except IOError as e:
            self.logger.error(f"读取配置文件失败: {e}")
            raise

    def get_love_quote_config(self):
        try:
            love_quote_section = self.config['LoveQuoteConfig']

            # 提取所有需要的配置项
            raw_config = {
                'SayLoveURL': love_quote_section.get('SayLoveURL'),
                'CaiHongPiURL': love_quote_section.get('CaiHongPiURL'),
                'Custom_Values': love_quote_section.get('Custom_Values'),
                'Max_Retries': love_quote_section.getint('Max_Retries')
            }

            # 处理 Custom_Values
            custom_values_str = raw_config['Custom_Values']
            custom_values = [value.strip() for value in custom_values_str.split(',')] if custom_values_str else []

            # 构建最终的配置字典
            love_quote_config = {
                'SayLoveURL': raw_config['SayLoveURL'],
                'CaiHongPiURL': raw_config['CaiHongPiURL'],
                'Custom_Values': custom_values,
                'Max_Retries': raw_config['Max_Retries']
            }

            return love_quote_config
        except (NoSectionError, NoOptionError) as e:
            self.logger.error(f"读取 LoveQuoteConfig 配置失败: {e}")
            raise

    def get_send_email_config(self):
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
            raise

    def get_event_config(self):
        try:
            event_section = self.config['EventConfig']

            raw_config = {
                'CalendarURL': event_section.get('CalendarURL'),
                'EventDays': self.json.loads(event_section.get('EventDays')),  # 使用实例变量 self.json
                'Day': event_section.getint('Day'),  # 显式转换为整数
                'Name': event_section.get('Name')
            }

            # 处理 Name
            Name_str = raw_config['Name']
            Name_str = [value.strip() for value in Name_str.split(',')] if Name_str else []

            # 构建最终的配置字典
            event_config = {
                'CalendarURL': raw_config['CalendarURL'],
                'EventDays': raw_config['EventDays'],
                'Day': raw_config['Day'],
                'Name': Name_str
            }

            return event_config
        except (NoSectionError, NoOptionError) as e:
            self.logger.error(f"读取 EventConfig 配置失败: {e}")
            raise


# 使用方法：
if __name__ == '__main__':
    try:
        reader = ConfigReader()
        print(reader.get_love_quote_config())
        print(reader.get_send_email_config())
        print(reader.get_event_config())
    except Exception as e:
        print(f"程序运行出错: {e}")