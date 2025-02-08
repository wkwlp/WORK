import os
from openai import OpenAI
from pushplus.config import *

class HunYuan:
    logger = setup_logger()

    def __init__(self, api_key=None, model="hunyuan-turbo"):
        """
        初始化 HunYuan 类。

        :param api_key: 可选参数，混元 API Key。如果未提供，则从环境变量 HunYuan_Key 获取。
        :param model: 使用的模型名称，默认是 "hunyuan-turbo"。
        """
        # 读取配置文件中的DeepSeek配置
        reader = ConfigReader()
        get_hunyuan_config = reader.get_hunyuan_config()
        self.url = get_hunyuan_config['URL']

        self.hunyuan_api_key = api_key or os.environ.get("HunYuan_Key")
        if not self.hunyuan_api_key:
            self.logger.error("未设置 HunYuan_Key 环境变量")
            raise ValueError("HunYuan_Key未设置")

        self.model = model

        # 构造 client
        self.client = OpenAI(
            api_key=self.hunyuan_api_key,
            base_url=self.url,
        )

    def send_message(self, message):
        """
        发送消息到混元 API 并获取回复。

        :param message: 用户输入的消息内容。
        :return: API 响应内容（字符串）或 None（请求失败时）。
        """
        # 检查并转换 message 参数为字典格式
        if not isinstance(message, dict):
            message = {"role": "user", "content": message}

        request_body = {
            "model": self.model,
            "messages": [message],
        }

        try:
            # 调用API并传递完整的请求体
            response = self.client.chat.completions.create(**request_body)
            # 检查响应是否包含有效的内容
            if hasattr(response, 'choices') and len(response.choices) > 0:
                return response.choices[0].message.content
            else:
                self.logger.error("API 响应中没有有效的 choices 字段")
                return None
        except Exception as e:
            self.logger.error(f"请求失败: {e}")
            return None

# 示例使用
if __name__ == "__main__":
    # turbo lite pro 模型可选
    hunyuan_client = HunYuan(model="hunyuan-turbo")

    user_message = "例如：目前实时天气为15度，明天预测天气为10-20度，请根据这些内容，帮我写一段温馨提示。内容要求：开头加上明日天气温馨提示：亲爱的老婆、限制40字以内、文字不需再编辑、文字内容不包含时间、温度、地区"

    response_content = hunyuan_client.send_message(user_message)
    print("Response Content:", response_content)