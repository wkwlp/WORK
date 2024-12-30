import logging
import os
import requests


class SendEmail:
    """
    通过PushPlus服务发送邮件提醒的类。

    Attributes:
        pushplus_token (str): PushPlus的服务Token。
    """
    logger = logging.getLogger(__name__)  # 创建一个与当前模块同名的日志记录器

    def __init__(self):
        """
        初始化WeatherReminderSender实例，从环境变量中读取PushPlus的服务Token。
        """
        self.pushplus_token = os.environ.get('PUSHPLUS_TOKEN')
        self.logger.info("SendEmail 初始化完成")

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
            # "topic": "wkwlp",  # 群组编码，如只需要个人接收，可注释这一行
            "template": "txt",  # 使用的邮件模板，此处使用纯文本格式
            "channel": "mail"  # 指定推送方式为邮件
        }
        # 设置请求头，告知服务器我们将发送JSON格式的数据
        headers = {'Content-Type': 'application/json'}
        # 使用POST方法发送数据，并获取响应对象
        response = requests.post(url, json=data, headers=headers)
        # 判断请求是否成功
        if response.status_code == 200:
            self.logger.info("邮件提醒发送成功")
        else:
            self.logger.error(f"邮件提醒发送失败，状态码：{response.status_code}")