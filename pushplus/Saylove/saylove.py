import requests
import os
import random
from pushplus.Weather.Weather import send_reminder_email


def get_random_love_quote(TIAN_KEY):
    """
    从天API获取一条随机情话。

    :param TIAN_KEY: 天API提供的API密钥。
    :return: 如果请求成功，则返回随机情话的字符串；否则返回None。
    """
    # 随机选择一个URL
    urls = [
        f'https://apis.tianapi.com/saylove/index?key={TIAN_KEY}',
        f'https://apis.tianapi.com/caihongpi/index?key={TIAN_KEY}'
    ]
    selected_url = random.choice(urls)

    try:
        # 发送HTTP GET请求
        response = requests.get(selected_url)

        # 检查请求是否成功
        if response.status_code == 200:
            # 解析返回的JSON数据
            quote_data = response.json()
            # 打印返回的json数据
            print(quote_data)

            # 尝试从返回的数据中提取情话内容
            content = quote_data.get('result', {}).get('content')

            # 如果找到了内容，返回去除空白字符的内容
            if content is not None:
                return f"致亲爱的老婆：{content.strip()}"

            # 如果没有找到content字段，打印提示信息
            print("返回的数据中没有找到'content'字段")

    except Exception as e:
        # 如果发生异常，打印错误信息
        print(f"发生错误：{e}")

    # 请求失败或未找到内容时返回None
    return None


if __name__ == "__main__":
    # 从环境变量中获取TIAN_KEY的Token
    TIAN_KEY = os.environ.get('TIAN_KEY')
    quote = get_random_love_quote(TIAN_KEY)

    # 发送邮件提醒
    send_reminder_email('每日小情话', quote)