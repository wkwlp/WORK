import os
import json
from configparser import ConfigParser, NoSectionError, NoOptionError
import logging
import inspect
from colorlog import ColoredFormatter

def setup_logger(level=logging.DEBUG):
    """
    配置并返回一个只输出到控制台且带有颜色的日志记录器。

    Args:
        level (int): 日志级别，默认为logging.INFO。

    Returns:
        logging.Logger: 配置好的日志记录器。
    """
    # 获取调用者的完整文件路径
    caller_frame = inspect.stack()[1][0]
    caller_filename = inspect.getframeinfo(caller_frame).filename
    full_path = os.path.abspath(caller_filename)  # 获取完整路径

    # 定义仓库根路径
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # 仓库根路径是当前文件的上一级目录

    # 获取相对于仓库根路径的相对路径
    relative_path = os.path.relpath(full_path, repo_root)

    # 将路径中的反斜杠 `\` 替换为点 `.`，并去掉文件扩展名
    module_style_path = relative_path.replace("\\", ".").replace("/", ".")
    module_style_path = module_style_path.replace(".py", "")  # 去掉 .py 后缀

    # 使用模块风格路径作为日志记录器的名称
    logger = logging.getLogger(module_style_path)
    logger.setLevel(level)

    # 如果已经存在处理器，则不再添加新的处理器
    if logger.hasHandlers():
        return logger

    # 设置日志格式，包含时间、日志级别、模块风格路径、行号和消息
    log_format = '%(log_color)s%(asctime)s [%(levelname)s] %(name)s.%(funcName)s:%(lineno)d - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'

    # 创建彩色日志格式器
    colored_formatter = ColoredFormatter(
        log_format,
        datefmt=date_format,
        reset=True,
        log_colors={
            'DEBUG': 'white',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )

    # 创建控制台处理器并设置格式
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(colored_formatter)

    # 添加处理器到记录器
    logger.addHandler(console_handler)

    return logger


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
                'Extensions': json.loads(weather_section.get('Extensions'))
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