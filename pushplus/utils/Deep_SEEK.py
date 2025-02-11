import os
from openai import OpenAI
import pushplus

class DeepSeek:
    """
    DeepSeek API 客户端简化版

    该类用于与DeepSeek API进行交互，生成对话响应。支持必填内容检查和流式模式。
    """
    def __init__(self):
        """
        初始化DeepSeek客户端。

        从配置文件中读取DeepSeek API的URL，并从环境变量中获取API密钥。
        如果未设置API密钥，则记录错误日志。
        """
        # 读取配置文件中的DeepSeek配置
        reader = pushplus.ConfigReader()
        config = reader.get_deep_seek_config()
        self.url = config['URL']
        self.logger = pushplus.setup_logger()
        # 从环境变量中获取DeepSeek API密钥
        self.deepseek_key = os.environ.get('DeepSeek_Key')
        if not self.deepseek_key:
            self.logger.error("未设置 DeepSeek_Key 环境变量")
            raise ValueError("DeepSeek_Key 环境变量未设置")

        # 初始化OpenAI客户端
        self.client = OpenAI(api_key=self.deepseek_key, base_url=self.url)

    def send_message(self, content: str, stream: bool = False) -> str:
        """
        生成对话响应。

        Args:
            content (str): 用户输入内容（必填，不能为空）
            stream (bool, optional): 是否使用流式传输，默认为False

        Returns:
            str: 生成的响应内容

        Raises:
            ValueError: 如果content为空或None
        """
        # 检查content是否为空
        if not content:
            self.logger.error("content不能为空")
            return ''

        # 创建聊天请求
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "user", "content": content}
            ],
            stream=stream
        )

        # 返回响应内容
        return response.choices[0].message.content


# 示例用法
if __name__ == "__main__":
    # 初始化DeepSeek客户端
    deepseek = DeepSeek()

    # 获取响应
    try:
        response = deepseek.send_message(content="今天是新年第一天开工，请告诉我，我应该注意哪些细节")
        print("答复:", response)
    except Exception as e:
        print(f"请求失败: {str(e)}")