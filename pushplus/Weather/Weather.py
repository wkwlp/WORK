import requests
from datetime import datetime, timedelta

def get_weather(amap_key):
    '''
    获取指定城市的天气信息

    :param amap_key: 高德地图API密钥
    :return: None
    '''

    # 获取昨天的日期
    yesterday = datetime.now() - timedelta(days=1)
    date_str = yesterday.strftime('%Y%m%d')

    # 构造请求 URL
    base_url = "https://restapi.amap.com/v3/weather/history"
    city = "南宁市"  # 目标城市名称

    # 完整的请求 URL 包括 API 密钥和其他参数
    complete_url = f"{base_url}?city={city}&date={date_str}&key={amap_key}"
    print(complete_url)
    # 发送 GET 请求并获取响应
    response = requests.get(complete_url)

    # 将 JSON 响应转换为 Python 字典
    data = response.json()

    if response.status_code == 200:
        # 检查请求是否成功
        if data.get('status') == '1':
            # 尝试获取历史天气信息
            try:
                history_weather = data['history'][0]
                print(f"昨天的历史天气信息:")
                print(f"日期: {yesterday.strftime('%Y-%m-%d')}")
                print(f"天气状况: {history_weather['weather']}")
                print(f"平均气温: {history_weather['avgTemp']}°C")
            except KeyError:
                print("没有找到昨天的历史天气信息。")
        else:
            # 如果请求失败，打印错误信息
            print("请求 API 失败:", data.get('infocode'), data.get('info'))
    else:
        # 如果 HTTP 请求失败，打印错误信息
        print("HTTP 请求失败:", response.status_code)


# 使用高德地图 API 密钥
amap_key = "c8a8f132a8d18c92b14c1e645145a3a8"
get_weather(amap_key)