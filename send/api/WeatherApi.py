import requests
import os
from typing import Optional, Dict, Tuple
import send
from fuzzywuzzy import process


class WeatherApi:
    """
    高德天气API服务封装类
    """

    # 常量定义
    MIN_SCORE = 50  # 模糊匹配最低置信度
    REQUEST_TIMEOUT = 10  # API请求超时时间(秒)

    def __init__(self):
        """
        初始化天气查询实例
        :raises ValueError: 当必要参数缺失时抛出
        """
        self.logger = send.setup_logger()

        try:
            config = send.ConfigReader().get_weather_config()
            self.url = config['URL']
            self.city_map = config['City']
            self.extensions_map = config['Extensions']
            self.output_format = config['Output'][0]
        except KeyError as e:
            self.logger.critical(f"关键配置项缺失: {e}")
            raise ValueError(f"配置文件不完整，缺失 {e} 配置项")

        self.weather_key = os.getenv('Weather_Key')
        if not self.weather_key:
            self.logger.error("未检测到Weather_Key环境变量")
            raise ValueError("Weather_Key环境变量未设置")

    def _parse_query(self, content: str) -> Tuple[Optional[str], Optional[str]]:
        """增强型模糊匹配解析器"""
        # 城市名称匹配分析
        city_scores = process.extract(content, self.city_map.keys())
        self.logger.debug(f"城市匹配: {city_scores}")
        # 气象类型匹配分析
        ext_scores = process.extract(content, self.extensions_map.keys())
        self.logger.debug(f"气象匹配: {ext_scores}")

        # 处理最佳匹配
        city_match = process.extractOne(content, self.city_map.keys())
        ext_match = process.extractOne(content, self.extensions_map.keys())

        self.logger.info(
            f"模糊匹配结果-最高候选:"
            f"城市: {city_match[0]}({city_match[1]}) "
            f"气象: {ext_match[0]}({ext_match[1]})"
        )

        return (
            self.city_map.get(city_match[0]) if city_match[1] >= self.MIN_SCORE else None,
            self.extensions_map.get(ext_match[0]) if ext_match[1] >= self.MIN_SCORE else None
        )

    def _build_api_url(self, content: str) -> Optional[str]:
        """
        构建API请求URL（含敏感信息脱敏处理）
        :return: 完整的API请求URL或None
        """
        city_code, ext_code = self._parse_query(content)
        if not all([city_code, ext_code]):
            self.logger.error("城市代码或气象类型代码缺失")
            return None

        params = {
            'city': city_code,
            'key': self.weather_key,
            'extensions': ext_code,
            'output': self.output_format
        }
        query_str = '&'.join([f"{key}={value}" for key, value in params.items()])
        complete_url = f'{self.url}?{query_str}'

        return complete_url

    def get_weather(self, content=None) -> Dict:
        """
        获取天气数据主入口
        :param content: 查询内容(格式：城市+气象类型)，示例："北京实时天气"
        :return: 结构化响应数据
        """
        if not content:
            self.logger.error("必须提供查询内容")
            return {
                'status': 400,
                'message': '请求内容不能为空，请求示例："南宁市预报天气"',
                'api': None
            }

        api_url = self._build_api_url(content)
        if not api_url:
            return {
                'status': 400,
                'message': 'URL不合法，请检查请求地址是否正确',
                'api': None
            }

        try:
            response = requests.get(
                api_url,
                timeout=self.REQUEST_TIMEOUT
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API请求失败: {str(e)}")
            return {
                'status': 500,
                'message': f"服务请求失败: {str(e)}",
                'api': None
            }

        try:
            result = response.json()
            if result.get('status') != '1':
                self.logger.error(f"API返回错误: {result.get('info')}")
                return {
                    'status': 502,
                    'message': result.get('info', '未知错误'),
                    'api': None
                }
        except ValueError:
            self.logger.error("响应数据解析失败")
            return {
                'status': 503,
                'message': '数据解析失败',
                'api': None
            }

        # 数据格式标准化
        return {
            'status': 200,
            'message': 'success',
            'api': {
                'lives': result.get('lives', []),
                'forecast': result.get('forecasts', [])
            }
        }


if __name__ == '__main__':
    # 示例用法
    weather_client = WeatherApi()
    result = weather_client.get_weather('南宁市预报天气')
    print(f"查询结果：{result}")