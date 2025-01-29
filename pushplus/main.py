from pushplus.controller import LoveQuoterController
from pushplus.utils import SendEmail
from pushplus.logger_config import setup_logger  # 从 pushplus 目录导入 setup_logger
import argparse


class PushPlus:
    def __init__(self, task_name):
        self.task_name = task_name
        self.logger = setup_logger()
        self.send_email = SendEmail()

    def handle_love_quote(self):
        """处理情话任务"""
        self.logger.info("开始处理情话任务")
        love_quoter_controller = LoveQuoterController()
        result = love_quoter_controller.handle_quote()

        if result['status'] == 200 and result.get('send_email', False):
            try:
                self.send_email.send_reminder_email('每日小情话', result['quote'], is_group_send=False)
                self.logger.info(f"邮件已发送, 内容：{result['quote']}")
            except Exception as e:
                self.logger.error(f"邮件发送失败，原因: {str(e)}")
        else:
            self.logger.warning(f"邮件发送失败，原因: {result.get('message', '未知错误')}")

    # def handle_event(self):
    #     """处理事件任务"""
    #     self.logger.info("开始处理事件任务")
    #     event_controller = EventController()
    #     result = event_controller.handle_event()
    #
    #     if result['status'] == 200 and result.get('send_email', False):
    #         try:
    #             self.send_email.send_reminder_email('事件提醒', result['event'], is_group_send=False)
    #             self.logger.info(f"邮件已发送, 内容：{result['event']}")
    #         except Exception as e:
    #             self.logger.error(f"邮件发送失败，原因: {str(e)}")
    #     else:
    #         self.logger.warning(f"邮件发送失败，原因: {result.get('message', '未知错误')}")

    def run(self):
        if self.task_name == 'love_quote':
            self.handle_love_quote()
        # elif self.task_name == 'event':
        #     self.handle_event()
        else:
            self.logger.error(f"未知的任务类型: {self.task_name}")


if __name__ == '__main__':
    # 默认任务为 'love_quote'
    default_task = 'love_quote'

    parser = argparse.ArgumentParser(description='PushPlus 任务运行器')
    parser.add_argument('task', type=str, choices=['love_quote', 'event'],
                        help='指定要运行的任务类型', nargs='?', default=default_task)

    args = parser.parse_args()

    # 实例化并运行 PushPlus 类
    push_plus = PushPlus(args.task)
    push_plus.run()