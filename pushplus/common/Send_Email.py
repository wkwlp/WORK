import os
import logging
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
        初始化SendEmail实例，从环境变量中读取PushPlus的服务Token。
        """
        self.pushplus_token = os.environ.get('PUSHPLUS_TOKEN')
        if not self.pushplus_token:
            self.logger.error("未设置 PUSHPLUS_TOKEN 环境变量")
            raise ValueError("PUSHPLUS_TOKEN 环境变量未设置")

        self.logger.info("SendEmail 初始化完成")

    def send_reminder_email(self, title, content, is_group_send=False):
        """
        通过PushPlus服务发送邮件提醒。

        Args:
            title (str): 邮件标题。
            content (str): 邮件内容。
            is_group_send (bool): 是否群组发送，默认为False（即个人接收）。
        """
        url = "http://www.pushplus.plus/send"
        data = {
            "token": self.pushplus_token,  # 推送使用的Token
            "title": title,  # 邮件标题
            "content": content,  # 邮件内容
            "template": "txt",  # 使用的邮件模板，此处使用纯文本格式
            "channel": "mail"  # 指定推送方式为邮件
        }

        # 如果是群组发送，则从环境变量获取topic并插入到data字典中
        if is_group_send:
            group_topic = os.environ.get('PUSHPLUS_GROUP_TOPIC')
            if not group_topic:
                self.logger.error("未设置 PUSHPLUS_GROUP_TOPIC 环境变量")
                raise ValueError("PUSHPLUS_GROUP_TOPIC 环境变量未设置")
            data["topic"] = group_topic

        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            self.logger.info("邮件提醒发送成功")
        else:
            self.logger.error(f"邮件提醒发送失败，状态码：{response.status_code}")