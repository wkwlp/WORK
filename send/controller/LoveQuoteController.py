import send


class LoveQuoteController:
    """
    负责业务逻辑判断并决定是否发送邮件的控制器类。

    该类接收情话内容，检查是否存在需要过滤的字段，并决定是否准备发送邮件。
    如果情话为None或包含过滤字段，则进行相应处理。
    """

    def __init__(self):
        """
        初始化LoveQuoterController实例。

        在初始化时，调用Service层获取初始情话。
        """
        self.logger = send.setup_logger()
        self.love_quote_service = send.LoveQuoteService()
        reader = send.ConfigReader()
        # 读取配置文件
        love_quote_config = reader.get_love_quote_config()
        self.custom_values, self.max_retries = love_quote_config['Custom_Values'], love_quote_config['Max_Retries']
        self.quote = self.get_initial_quote()

    def get_initial_quote(self):
        """
        获取初始情话。

        :return: 从Service层获取的情话字符串，如果获取失败则返回None。
        """
        try:
            initial_quote = self.love_quote_service.get_quote()
            return initial_quote
        except Exception as e:
            self.logger.error(f"获取初始情话时发生错误: {e}")
            return None

    def handle_quote(self):
        """
        进行业务逻辑判断并决定是否发送邮件。

        如果情话中包含任何需要过滤的字段，则重新调用API获取新数据。
        如果连续3次都包含过滤字段，则返回默认内容。
        否则，准备发送邮件并返回成功状态码及情话内容。

        :return: 包含状态码、消息和情话内容的结果字典。
        """
        retries = 0

        while retries < self.max_retries:
            if not self.quote:
                self.logger.warning("无法获取有效的情话数据，返回默认数据")
                self.quote = f"致亲爱的老婆：今天接口有问题，我亲口跟你说：我永远爱你！"
                break

            if any(value in self.quote for value in self.custom_values):
                self.logger.warning(f"情话包含不合适的词语: {self.custom_values}")
                retries += 1
                if retries >= self.max_retries:
                    self.quote = f"致亲爱的老婆：今天接口有问题，我亲口跟你说：我永远爱你！"
                    break
                # 重新获取情话
                self.quote = self.get_initial_quote()
                self.logger.warning(f"重新获取的情话为: {self.quote}")
            else:
                break

        if self.quote:
            return {'status': 200, 'message': '邮件准备发送', 'quote': self.quote, 'send_email': True}
        else:
            return {'status': 400, 'message': '无法获取有效的情话数据'}