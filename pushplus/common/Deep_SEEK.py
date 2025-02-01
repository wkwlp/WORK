from openai import OpenAI

class DeepSeek:
    """
    DeepSeek API 客户端简化版

    用于生成对话响应，支持必填内容检查和流式模式
    """

    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com"):
        """
        初始化客户端

        Args:
            api_key (str): DeepSeek API密钥
            base_url (str, optional): API基础地址，默认为DeepSeek官方地址
        """
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def generate_response(self, content: str, stream: bool = False) -> str:
        """
        生成对话响应

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
            raise ValueError("content不能为空")

        # 创建聊天请求
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                # {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": content}
            ],
            stream=stream
        )

        # 返回响应内容
        return response.choices[0].message.content


# # 示例用法
# if __name__ == "__main__":
#     # 初始化客户端
#     deepseek = DeepSeek(CalendarKEY="sk-b416e4a8c2a7413caf8c87a5fcf2c57f")
#
#     # 获取响应
#     try:
#         response = deepseek.generate_response(content="Hello")
#         print("Assistant:", response)
#     except ValueError as e:
#         print(f"输入错误: {str(e)}")
#     except Exception as e:
#         print(f"API请求失败: {str(e)}")