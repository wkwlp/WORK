from pushplus.controller import LoveQuoterController
from pushplus.utils import SendEmail
from pushplus.logger_config import setup_logger  # 从 pushplus 目录导入 setup_logger

# 设置日志记录器
logger = setup_logger()

def main():
    # 初始化控制器层
    love_quoter_controller = LoveQuoterController()

    # 获取处理后的情话
    result = love_quoter_controller.handle_quote()

    if result['status'] == 200 and result.get('send_email', False):
        try:
            # 初始化邮件发送工具
            send_email = SendEmail()

            # 发送邮件
            send_email.send_reminder_email('每日小情话', result['quote'], is_group_send=False)
            logger.info(f"邮件已发送, 内容：{result['quote']}")
        except Exception as e:
            logger.error(f"邮件发送失败，原因: {str(e)}")
    else:
        logger.warning(f"邮件发送失败，原因: {result.get('message', '未知错误')}")


if __name__ == '__main__':
    main()