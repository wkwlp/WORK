import pymysql
from pymysql.cursors import DictCursor
from typing import  Optional, Any


class DatabaseManager:
    def __init__(self, host: str, port: int, user: str, password: str, db: str, charset: str = 'utf8mb4'):
        self.db_config = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "db": db,
            "charset": charset,
            "cursorclass": DictCursor
        }
        self.connection: Optional[pymysql.connections.Connection] = None

    def __enter__(self):
        """上下文管理器进入时调用"""
        if not self.connect():
            raise RuntimeError("无法建立数据库连接")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出时调用"""
        self.close()

    def connect(self) -> bool:
        """建立数据库连接"""
        try:
            self.connection = pymysql.connect(**self.db_config)
            return True
        except pymysql.MySQLError as e:
            print(f"数据库连接出错: {e}")
            return False

    def fetch_data(self, fsnr: str) -> tuple[tuple[Any, ...], ...] | list[Any]:
        """根据fsnr查询数据"""
        if not self.connection:
            raise RuntimeError("请先调用connect方法建立连接")

        sql = "SELECT a.* FROM send_hz a WHERE fsnr = %s"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, (fsnr,))
                results = cursor.fetchall()
                return results
        except pymysql.MySQLError as e:
            print(f"数据库操作出错: {e}")
            return []

    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()

# 使用示例
