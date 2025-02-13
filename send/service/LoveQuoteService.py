import send


class LoveQuoteService:
    """
    处理从天API获取的随机情话的服务类。

    该类负责调用外部API获取随机情话，并对返回的数据进行处理，最终返回格式化后的情话内容。
    """

    def __init__(self):
        """
        初始化LoveQuoteService实例。

        在初始化时，会创建一个LoveQuoteApi实例用于后续获取情话数据。
        """
        self.logger = send.setup_logger()
        self.love_quote_api = send.LoveQuoteApi()

    def get_quote(self):
        """
        获取并处理一条随机情话。

        该方法首先通过LoveQuoteApi实例获取随机情话数据，然后调用handle_quote方法处理这些数据，
        最终返回格式化后的情话字符串。如果在过程中遇到任何问题，则返回None。

        :return: 返回处理后的情话字符串，如果没有找到合适的内容则返回None。
        """
        try:
            # 调用API获取随机情话数据
            quote_data = self.love_quote_api.get_random_quote()

            # 处理获取到的情话数据
            content = self.handle_quote(quote_data)
            if not content:
                self.logger.warning("获取情话中content为空,返回None")
                return None

            # 返回去除空白字符后的情话内容
            return f"致亲爱的老婆：{content.strip()}"

        except Exception as e:
            # 记录错误日志并返回None
            self.logger.error(f"处理情话时发生错误: {e}")
            return None

    def handle_quote(self, quote):
        """
        从API响应数据中提取情话内容。

        该方法接收API响应的数据字典，检查其有效性并从中提取情话内容。如果数据无效或缺少必要字段，
        则记录相应的警告信息并返回None。

        :param quote: API响应的数据字典。
        :return: 提取到的情话内容，如果未找到或无效则返回None。
        """
        # 检查quote数据是否有效且包含'result'字段
        if not quote or 'result' not in quote:
            self.logger.warning("无法获取有效的情话数据")
            return None

        # 尝试从result字段中提取content
        content = quote['result'].get('content')
        if not content:
            self.logger.warning("返回的数据中没有找到content字段")
            return None

        # 返回提取到的情话内容
        self.logger.info("成功获取情话内容: %s", content)
        return content