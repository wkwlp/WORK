import send
import argparse


class PushPlus:

    def __init__(self, task_name):
        self.task_name = task_name
        self.logger = send.setup_logger()
        self.send_email = send.PushPlus()
        self.love_mysql = send.LoveMysql()

    def handle_love_quote(self):
        """处理情话任务"""
        self.logger.info("开始处理情话任务")
        # 获取情话
        love_quoter_controller = send.LoveQuoteController()
        result = love_quoter_controller.handle_quote()

        if result['status'] == 200 and result.get('send_email', False):
            try:
                # self.send_email.send_reminder_email('每日小情话', result.get('quote'), is_group_send=False)
                self.logger.info(f"邮件已发送, 内容：{result['quote']}")
                self.love_mysql.update_love_hz(hzbh=result.get('hzbh'),fsnr=result.get('quote'),fszt=result.get('fszt'))
            except Exception as e:
                self.logger.error(f"邮件发送失败，原因: {str(e)}")
                self.love_mysql.update_love_hz(hzbh=result.get('hzbh'),fsnr=result.get('message'),fszt=result.get('fszt'))
        else:
            self.logger.warning(f"邮件发送失败，原因: {result.get('message', '未知错误')}")
            self.love_mysql.update_love_hz(hzbh=result.get('hzbh'),fsnr=result.get('message'),fszt=result.get('fszt'))

    def handle_event(self):
        """处理事件任务"""
        self.logger.info("开始处理事件任务")
        # 获取日历信息
        event_service = send.EventService()
        calendar_content = event_service.get_calendar() # 默认使用明天的日期

        if calendar_content['status'] == 200 and calendar_content.get('send_email', False):
            try:
                # self.send_email.send_reminder_email('节日提醒', calendar_content.get('calendar_content'), is_group_send=False)
                self.logger.info(f"邮件已发送, 内容：{calendar_content['calendar_content']}")
            except Exception as e:
                self.logger.error(f"邮件发送失败，原因: {str(e)}")
        else:
            self.logger.warning(f"邮件发送失败，原因: {calendar_content.get('message', '未知错误')}")

        # 处理事件信息
        event_controller = send.EventController()
        events = event_controller.get_events()
        content = event_controller.handle_content(events)

        if content['status'] == 200 and content.get('send_email', False):
            try:
                self.send_email.send_reminder_email('事件提醒', content.get('content'), is_group_send=False)
                self.logger.info(f"邮件已发送, 内容：{content['content']}")
            except Exception as e:
                self.logger.error(f"邮件发送失败，原因: {str(e)}")
        else:
            self.logger.warning(f"邮件发送失败，原因: {content.get('message', '未知错误')}")
    def handle_weather(self):
        self.logger.info("开始处理天气任务")
        weather_controller = send.WeatherController()
        weather = weather_controller.get_weather()
        if weather:
            try:
                # self.send_email.send_reminder_email(title='天气提醒', content=weather, is_group_send=False)
                self.logger.info(f"邮件已发送, 内容：{weather}")
            except Exception as e:
                self.logger.error(f"邮件发送失败，原因: {str(e)}")
        else:
            self.logger.warning(f"邮件发送失败，原因: 无法获取天气信息")

    def run(self):
        if self.task_name == 'love_quote':
            self.handle_love_quote()
        elif self.task_name == 'event':
            self.handle_event()
        elif self.task_name == 'weather':
            self.handle_weather()
        else:
            self.logger.error(f"未知的任务类型: {self.task_name}")


if __name__ == '__main__':
    # 默认任务为 'love_quote'
    default_task = 'love_quote'

    parser = argparse.ArgumentParser(description='PushPlus 任务运行器')
    parser.add_argument('task', type=str, choices=['love_quote', 'event','weather'],
                        help='指定要运行的任务类型', nargs='?', default=default_task)

    args = parser.parse_args()

    # 实例化并运行 PushPlus 类
    push_plus = PushPlus(args.task)
    push_plus.run()