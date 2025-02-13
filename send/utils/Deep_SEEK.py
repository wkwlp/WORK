import os
import openai
import send


class DeepSeek:
    """
    DeepSeek API 客户端简化版

    该类用于与DeepSeek API进行交互，生成对话响应。支持必填内容检查。
    """

    def __init__(self, model="deepseek-chat"):
        """
        初始化DeepSeek客户端。

        从配置文件中读取DeepSeek API的URL，并从环境变量中获取API密钥。
        如果未设置API密钥，则记录错误日志。
        """
        # 读取配置文件中的DeepSeek配置
        reader = send.ConfigReader()
        config = reader.get_deep_seek_config()
        self.url = config['URL']
        self.logger = send.setup_logger()
        # 从环境变量中获取DeepSeek API密钥
        self.deepseek_key = os.environ.get('DeepSeek_Key')
        if not self.deepseek_key:
            self.logger.error("未设置 DeepSeek_Key 环境变量")
            raise ValueError("DeepSeek_Key 环境变量未设置")
        self.model = model
        # 设置OpenAI API密钥和基础URL
        self.client = openai.OpenAI(api_key=self.deepseek_key, base_url=self.url)

    def send_message(self, content: str):
        """
        生成对话响应。

        Args:
            content (str): 用户输入内容（必填，不能为空）

        Returns:
            str or None: 生成的响应内容或None（如果请求失败）

        Raises:
            ValueError: 如果content为空或None
        """
        # 检查content是否为空
        if not content:
            self.logger.error("内容不能为空")
            return None

        try:
            # 创建聊天请求（默认为非流式）
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": content}
                ]
            )

            self.logger.info(f"响应内容:{response}")
            # 处理非流式响应
            full_response = response.choices[0].message.content
            return full_response

        except openai.OpenAIError as e:
            # 处理OpenAI API相关错误
            self.logger.error(f"OpenAI API 错误: {e}")
            return None
        except Exception as e:
            # 处理其他可能的异常
            self.logger.error(f"发生错误: {e}")
            return None


# 示例：如何使用 DeepSeek 类
if __name__ == "__main__":
    # 创建 DeepSeek 实例
    deep_seek_client = DeepSeek()

    # 发送消息并接收响应
    response = deep_seek_client.send_message(content="你好，今天天气怎么样？")

    if response is not None:
        print(f"收到的回复: {response}")
    else:
        print("未能获取到回复")