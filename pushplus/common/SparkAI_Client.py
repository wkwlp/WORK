# 从sparkai的llm模块中导入ChatSparkLLM类以及ChunkPrintHandler类。
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler

# 同样从sparkai的核心消息模块中导入ChatMessage类，用于创建聊天消息对象。
from sparkai.core.messages import ChatMessage

class SparkAIClient:
    def __init__(self):
        # 定义连接到SparkAI服务的URL、应用ID、API密钥等信息。
        self.SPARKAI_URL = 'wss://spark-api.xf-yun.com/v1.1/chat'
        self.SPARKAI_APP_ID = 'fa231aa7'
        self.SPARKAI_API_SECRET = 'YmQzMzA2OWFhZWIzY2E4NDc1MzQ5YTI0'
        self.SPARKAI_API_KEY = 'f3d97121e74d4b8b48c9f11ea6e1745e'
        self.SPARKAI_DOMAIN = 'lite'

        # 创建一个ChatSparkLLM实例，它代表了与SparkAI服务的会话。
        self.spark = ChatSparkLLM(
            spark_api_url=self.SPARKAI_URL,
            spark_app_id=self.SPARKAI_APP_ID,
            spark_api_key=self.SPARKAI_API_KEY,
            spark_api_secret=self.SPARKAI_API_SECRET,
            spark_llm_domain=self.SPARKAI_DOMAIN,
            streaming=False,  # 流式传输设置为False表示不使用流式传输。
        )

    def generate_text(self, content: str) -> str:
        """
        接收用户输入的字符串内容，调用SparkAI服务生成回复，并返回生成的文本。

        :param content: 用户输入的字符串内容
        :return: 生成的文本
        """
        # 创建一个包含单个用户消息的消息列表。
        messages = [ChatMessage(
            role="user",
            content=content
        )]

        # 创建一个ChunkPrintHandler实例，用于处理生成的响应。
        handler = ChunkPrintHandler()

        # 调用generate方法，并将结果存储在response变量中
        response = self.spark.generate([messages], callbacks=[handler])

        try:
            # 检查response对象是否有generations属性并且该属性非空
            if hasattr(response, 'generations') and response.generations:
                generated_texts = []
                for generation_list in response.generations:
                    for chat_generation in generation_list:
                        # 检查chat_generation对象是否有text属性
                        if hasattr(chat_generation, 'text'):
                            generated_texts.append(chat_generation.text)
                return "\n".join(generated_texts) if generated_texts else "未找到任何生成的文本。"
            else:
                return "未找到任何生成的文本。"
        except Exception as e:
            return f"处理响应时出错: {e}"

# 示例使用
if __name__ == '__main__':
    client = SparkAIClient()
    user_input = "你好呀"
    generated_text = client.generate_text(user_input)
    print(f"生成的文本:\n{generated_text}")