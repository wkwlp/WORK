import requests

def get_weather(amap_key):
    '''

    :param amap_key:
    :return:
    '''
    # 构造请求 URL
    base_url = "https://restapi.amap.com/v3/weather/weatherInfo"
    city = "南宁市"  # 目标城市名称

    # 完整的请求 URL 包括 API 密钥和其他参数
    complete_url = f"{base_url}?city={city}&key={amap_key}"

    # 发送 GET 请求并获取响应
    response = requests.get(complete_url)

    # 将 JSON 响应转换为 Python 字典
    data = response.json()

    if response.status_code == 200:
        # 检查请求是否成功
        if data.get('status') == '1':
            # 尝试获取实时天气信息
            try:
                live_weather = data['lives'][0]
                print(f"实时天气信息:")
                print(f"温度: {live_weather['temperature']}°C")
                print(f"风力等级: {live_weather['windpower']}")
            except KeyError:
                    print("没有找到实时天气信息或天气预报信息。")
        else:
            # 如果请求失败，打印错误信息
            print("请求 API 失败:", data.get('infocode'), data.get('info'))
    else:
        # 如果 HTTP 请求失败，打印错误信息
        print("HTTP 请求失败:", response.status_code)


# 使用高德地图 API 密钥
amap_key = "c8a8f132a8d18c92b14c1e645145a3a8"
get_weather(amap_key)