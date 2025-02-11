import os
import requests
import pushplus

__all__ = ['SendEmail']

class SendEmail:
    """
    通过PushPlus服务发送邮件提醒的类。

    Attributes:
        pushplus_token (str): PushPlus的服务Token。
        url (str): 发送邮件的URL。
        template (str): 使用的邮件模板。
        channel (str): 推送方式（如邮件）。
    """

    def __init__(self):
        """
        初始化SendEmail实例，从环境变量中读取PushPlus的服务Token，并从config.ini文件中读取其他配置项。
        """
        self.logger = pushplus.setup_logger()
        reader = pushplus.ConfigReader()
        # 读取配置文件中的URL、模板和推送方式
        get_send_email_config = reader.get_send_email_config()
        self.url, self.template,self.channel = (get_send_email_config['URL'], get_send_email_config['Template'],
                                                get_send_email_config['Channel'])

        # 从环境变量中读取PushPlus的服务Token
        self.pushplus_token = os.environ.get('PUSHPLUS_TOKEN')
        if not self.pushplus_token:
            self.logger.error("未设置 PUSHPLUS_TOKEN 环境变量")

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
