from pushplus.logger_config import setup_logger
from pushplus.service import *
from pushplus.config import *
from datetime import datetime

class EventController:
    """
    负责业务逻辑判断并决定是否发送邮件的控制器类。

    该类接收情话内容，检查是否存在需要过滤的字段，并决定是否准备发送邮件。
    如果情话为None或包含过滤字段，则进行相应处理。
    """

    def __init__(self):
        """
        初始化EventController实例。

        在初始化时，调用Service层获取初始情话。
        """
        self.logger = setup_logger()
        self.event_service = EventService()
        config = ConfigReader()
        self.day = int(config.get_event_config()['Day'])  # 确保day是整数

    def get_events(self):
        """
        获取所有事件及其与当前日期的差值。

        返回:
            一个列表，每个元素是一个字典，包含name、date以及与当前日期的天数差(diff_days)。
            如果事件名称中包含'重要'或'紧急'，则diff_days设置为0。
        """
        events = self.event_service.handle_events()
        today = datetime.now().date()

        if not events:
            return []

        for event in events:
            name = event['name']
            date_str = event['date']

            if '重要' in name or '紧急' in name:
                # 对于重要或紧急事件，直接将diff_days设置为0
                event['diff_days'] = 0
            else:
                try:
                    event_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    diff_days = (event_date - today).days
                    event['diff_days'] = diff_days
                except ValueError:
                    # 如果日期格式不正确，记录错误并跳过该事件
                    self.event_service.logger.error(f"无法解析日期 {date_str} 对应的事件 {name}")
                    continue

        return events

    def handle_content(self, events):
        """
        根据事件列表构建通知内容。

        参数:
            events (list): 包含事件信息的列表，每个元素是一个字典，包含name、date和diff_days。

        返回:
            content (str): 构建的通知内容字符串。
        """
        notification_items = []
        for event in events:
            name = event['name']
            date = event['date']
            date_str = event['date_str']
            diff_days = event['diff_days']

            if diff_days == 0 or (isinstance(diff_days, int) and 0 < diff_days <= self.day):
                if diff_days == 0:
                    item = f"{name}: {date_str}"
                else:
                    item = f"{name}: {date_str}（公历日期：{date}，距离今天{diff_days}天）"
                notification_items.append(item)

        if not notification_items:
            self.logger.info("未来七天内未有事件")
            return None

        content = "未来有以下日子需要注意：\n" + "\n".join(notification_items)
        return content

# 示例调用
if __name__ == "__main__":
    event_controller = EventController()
    events = event_controller.get_events()
    content = event_controller.handle_content(events)
    print(content)