import os
import requests
from pathlib import Path
import configparser
from pushplus.logger_config import setup_logger  # 导入日志配置模块

class SendEmail:
    """
    通过PushPlus服务发送邮件提醒的类。

    Attributes:
        pushplus_token (str): PushPlus的服务Token。
        url (str): 发送邮件的URL。
        template (str): 使用的邮件模板。
        channel (str): 推送方式（如邮件）。
    """
    logger = setup_logger()  # 创建一个与当前模块同名的日志记录器

    def __init__(self):
        """
        初始化SendEmail实例，从环境变量中读取PushPlus的服务Token，并从config.ini文件中读取其他配置项。
        """
        # 读取配置文件
        try:
            config = self._read_config()
        except (FileNotFoundError, KeyError, configparser.Error) as e:
            self.logger.error(f"读取配置文件时发生错误: {e}")
            raise

        # 读取配置文件中的URL、模板和推送方式
        self.url = config['SendEmailConfig']['URL']
        self.template = config['SendEmailConfig']['Template']
        self.channel = config['SendEmailConfig']['Channel']

        # 从环境变量中读取PushPlus的服务Token
        self.pushplus_token = os.environ.get('PUSHPLUS_TOKEN')
        if not self.pushplus_token:
            self.logger.error("未设置 PUSHPLUS_TOKEN 环境变量")
            raise ValueError("PUSHPLUS_TOKEN 环境变量未设置")

        self.logger.info("SendEmail 初始化完成")

    def _read_config(self):
        """
        读取配置文件并返回ConfigParser对象。

        Returns:
            ConfigParser: 配置文件解析后的对象。
        """
        # 使用相对路径读取配置文件
        config_path = Path(__file__).resolve().parents[1] / 'config.ini'

        if not config_path.exists():
            self.logger.error(f"配置文件不存在: {config_path}")
            raise FileNotFoundError(f"配置文件不存在: {config_path}")

        config = configparser.ConfigParser()

        try:
            config.read(config_path)
        except configparser.Error as e:
            self.logger.error(f"读取配置文件时发生错误: {e}")
            raise

        # 检查配置文件中是否存在 SendEmailConfig section
        if not config.has_section('SendEmailConfig'):
            self.logger.error("配置文件中缺少 'SendEmailConfig' section")
            raise KeyError("配置文件中缺少 'SendEmailConfig' section")

        return config

    def send_reminder_email(self, title, content, is_group_send=False):
        """
        通过PushPlus服务发送邮件提醒。

        Args:
            title (str): 邮件标题。
            content (str): 邮件内容。
            is_group_send (bool): 是否群组发送，默认为False（即个人接收）。
        """
        data = {
            "token": self.pushplus_token,  # 推送使用的Token
            "title": title,  # 邮件标题
            "content": content,  # 邮件内容
            "template": self.template,  # 使用的邮件模板，此处使用纯文本格式
            "channel": self.channel  # 指定推送方式为邮件
        }

        # 如果是群组发送，则从环境变量获取topic并插入到data字典中
        if is_group_send:
            group_topic = os.environ.get('PUSHPLUS_GROUP_TOPIC')
            if not group_topic:
                self.logger.error("未设置 PUSHPLUS_GROUP_TOPIC 环境变量")
                raise ValueError("PUSHPLUS_GROUP_TOPIC 环境变量未设置")
            data["topic"] = group_topic

        headers = {'Content-Type': 'application/json'}
        response = requests.post(self.url, json=data, headers=headers)

        if response.status_code == 200:
            self.logger.info("邮件提醒发送成功")
        else:
            self.logger.error(f"邮件提醒发送失败，状态码：{response.status_code}")
            self.logger.error(f"响应内容：{response.text}")
