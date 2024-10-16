import requests

def get_weather(amap_key):
    '''
    获取天气信息，并根据返回的数据类型打印实时或预报天气。

    :param amap_key: 高德地图API密钥
    '''
    # 构造请求 URL
    base_url = "https://restapi.amap.com/v3/weather/weatherInfo"
    city = "450103"  # 南宁市青秀区
    extensions = 'all'  # all:返回预报天气 base:返回实况天气
    output = 'json'  # 返回格式

    # 完整的请求 URL 包括 API 密钥和其他参数
    complete_url = f"{base_url}?city={city}&key={amap_key}&extensions={extensions}&output={output}"
    print(complete_url)

    # 发送 GET 请求并获取响应
    response = requests.get(complete_url)

    # 将 JSON 响应转换为 Python 字典
    data = response.json()
    print(data)

    if response.status_code == 200:
        # 检查请求是否成功
        if data.get('status') == '1':
            if 'lives' in data:
                # 获取实时天气信息
                print("实时天气信息:")
                for live_weather in data['lives']:
                    print(f"天气发布时间: {live_weather['reporttime']}")
                    print(f'地区：{live_weather["province"]}南宁市{live_weather["city"]}')
                    print(f"温度: {live_weather['temperature']}°C")
                    print(f"风力等级: {live_weather['windpower']}")

            elif 'forecasts' in data:
                # 获取预报天气信息
                forecasts = data['forecasts'][0]
                print(f"预报天气信息:")
                for forecast in forecasts['casts']:
                    print(f"日期: {forecast['date']}")
                    print(f"天气状况: {forecast['dayweather']} / {forecast['nightweather']}")
                    print(f"白天温度: {forecast['daytemp']}°C")
                    print(f"夜间温度: {forecast['nighttemp']}°C")
            else:
                print("没有找到天气信息。")
        else:
            # 如果请求失败，打印错误信息
            print("请求 API 失败:", data.get('infocode'), data.get('info'))
    else:
        # 如果 HTTP 请求失败，打印错误信息
        print("HTTP 请求失败:", response.status_code)

# 使用高德地图 API 密钥
amap_key = "c8a8f132a8d18c92b14c1e645145a3a8"
get_weather(amap_key)