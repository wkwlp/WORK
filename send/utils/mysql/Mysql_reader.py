from typing import Optional, List, Union
from send.utils.mysql.Mysql import MysqlOperations
import send
from datetime import datetime

logger = send.setup_logger()
mysql_ops = MysqlOperations()

class LoveMysql:
    def __init__(self):
        self.mysql_ops = mysql_ops

    def _select(self, table: str, columns: List[str], conditions: dict, return_type: str = 'list'):
        try:
            results = self.mysql_ops.select(table, columns, conditions, return_type)
            return results
        except Exception as e:
            logger.error(f"查询数据失败: {e}")
            return None

    def select_love_url(self, return_type: str = 'list') -> Optional[List]:
        """
        查询SEND_DM表中的love类型的KC1字段。
        :return: 查询结果列表
        """
        table = "SEND_DM"
        columns = ["KC1"]
        conditions = {"DMLB": "love", "DM": ["01", '02'], 'SYZT': 1}
        return self._select(table, columns, conditions, return_type)

    def select_love_word(self) -> Optional[List]:
        """
        查询SEND_DM表中的love类型的DMMC字段。
        :return: 查询结果列表
        """
        table = "SEND_DM"
        columns = ["DMMC"]
        conditions = {"DMLB": "love", "DM": "love_word", 'SYZT': 1}
        result = self._select(table, columns, conditions)

        if result is None or result == []:
            return None
        custom_values = result[0].split(',')

        # 提取查询结果中的DMMC字段值并返回
        return custom_values

    def select_love_count(self) -> Optional[Union[int, List]]:
        """
        查询SEND_DM表中的love类型的count字段。
        :return: 查询结果列表或整数
        """
        table = "SEND_DM"
        columns = ["DMMC"]
        conditions = {"DMLB": "love", "DM": "count", 'SYZT': 1}
        return self._select(table, columns, conditions, 'int')

    def insert_love_api(self, url_name: Optional[str] = None, response: Optional[str] = None) -> str:
        now = datetime.now()
        hzbh = now.strftime('%Y%m%d%H%M%S%f')
        insert_values = {
            "HZBH": hzbh,
            "URL_NAME": url_name,
            "YWLX": 'love',
            "RESPONSE": response,
            "FSSJ": now
        }
        self.mysql_ops.insert("SEND_DATA", insert_values)
        return hzbh

    def insert_love_hz(self, hzbh: str, fszt: str, fsnr: Optional[str] = None) -> str:
        now_czsj = datetime.now()
        insert_values = {
            "HZBH": hzbh,
            "FSNR": fsnr,
            "CZSJ": now_czsj,
            "YWLX": 'love',
            "FSZT": fszt
        }
        self.mysql_ops.insert("SEND_HZ", insert_values)
        return hzbh

    def update_love_hz(self, hzbh: str, fszt: str, fsnr: Optional[str] = None):
        now_fssj = datetime.now()
        update_values = {
            "FSZT": fszt,
            "FSNR": fsnr,
            'FSSJ': now_fssj
        }
        conditions = {"HZBH": hzbh}
        self.mysql_ops.update("SEND_HZ", update_values, conditions)

    def update_love_api(self, hzbh: str, quote: Optional[str] = None):
        update_values = {"QUOTE": quote}
        conditions = {"HZBH": hzbh}
        self.mysql_ops.update("SEND_DATA", update_values, conditions)

if __name__ == '__main__':
    a = LoveMysql()
    b = a.select_love_word()
    logger.info(b)

