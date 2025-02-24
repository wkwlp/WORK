import pymysql
from pymysql.cursors import DictCursor
from typing import Optional, Any, List, Dict, Union
import send
from datetime import datetime
import os


class MysqlConnection:
    def __init__(self):
        self.logger = send.setup_logger()
        # 解析环境变量并构建数据库配置字典
        self.db_config = self._build_db_config()
        # 初始化连接对象，初始为 None
        self.connection: Optional[pymysql.connections.Connection] = None

    def _build_db_config(self):
        """
        从环境变量中读取数据库连接信息并构建配置字典。
        """

        def parse_host_port(host_port_str):
            host, port = host_port_str.split(':')
            return host, int(port)

        def parse_user_password(user_password_str):
            user, password = user_password_str.split(':')
            return user, password

        # 读取环境变量
        host_port_str = os.getenv("HOSTPORT")
        user_password_str = os.getenv("USER_PASSWORD")

        if not host_port_str or not user_password_str:
            self.logger.error("必须设置 HOST_PORT 和 USER_PASSWORD 环境变量")

        # 解析环境变量
        host, port = parse_host_port(host_port_str)
        user, password = parse_user_password(user_password_str)

        # 构建数据库配置字典
        db_config = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "db": "send",
            "charset": "utf8mb4",
            "cursorclass": DictCursor
        }

        return db_config

    def __enter__(self):
        """上下文管理器进入时调用，尝试建立数据库连接"""
        try:
            # 建立数据库连接
            self.connection = pymysql.connect(**self.db_config)
            return self.connection
        except pymysql.MySQLError as e:
            # 连接出错时打印错误信息
            self.logger.error(f"数据库连接出错: {e}")
            raise RuntimeError("无法建立数据库连接")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出时调用，关闭数据库连接"""
        if self.connection:
            self.connection.close()


class MysqlOperations:
    def __init__(self):
        # 初始化 MysqlConnection 实例
        self.logger = send.setup_logger()
        self.db_connection = MysqlConnection()

    def select(self, table: str, columns: Optional[List[str]] = None, conditions: Optional[Dict[str, Any]] = None,
               return_type: str = 'list'):
        """
        根据条件查询特定列的数据，支持无条件查询，并支持返回单个整数值。
        :param table: 表名
        :param columns: 要查询的列名列表，默认为None表示查询所有列
        :param conditions: 查询条件，字典类型，键为列名，值为对应的值，默认为None表示无条件查询
        :param return_type: 返回数据的类型，list、dict 或 int，默认为 list。如果选择int，则返回特定列的第一个值。
        :return: 查询结果或特定配置项的整数值
        """
        if columns is None or len(columns) == 0:
            cols = '*'
        else:
            cols = ', '.join(columns)

        where_clause = ""
        params = ()

        if conditions is not None and len(conditions) > 0:
            where_clauses = []
            param_values = []
            for k, v in conditions.items():
                if isinstance(v, list):
                    placeholders = ', '.join(['%s'] * len(v))
                    where_clauses.append(f"{k} IN ({placeholders})")
                    param_values.extend(v)
                else:
                    where_clauses.append(f"{k} = %s")
                    param_values.append(v)

            where_clause = ' AND '.join(where_clauses)
            params = tuple(param_values)

        sql = f"SELECT {cols} FROM {table}" + (f" WHERE {where_clause}" if where_clause else "")
        self.logger.info(f'SELECT_SQL: {sql}')

        if conditions is not None and len(conditions) > 0:
            formatted_params = [f"{v}({type(v).__name__})" for v in params]
            self.logger.info(f"PARAMS: {', '.join(formatted_params)}")

        with self.db_connection as conn:
            try:
                with conn.cursor() as cursor:
                    total = cursor.execute(sql, params)
                    self.logger.info(f"TOTAL: {total}")  # 记录总数日志
                    results = cursor.fetchall()
                    if return_type == 'int':
                        if len(results) > 0:
                            # 提取第一条记录的第一个字段并尝试转换为整数
                            first_row = results[0]
                            first_value = list(first_row.values())[0] if isinstance(first_row, dict) else first_row[0]
                            return int(first_value)
                        else:
                            self.logger.warning("没有找到记录，返回None")
                            return None  # 如果没有找到记录，则返回None

                    if return_type == 'dict':
                        return results  # 直接返回查询结果

                    # 处理 list 返回类型
                    if not columns or len(columns) == 0:
                        raise ValueError("返回列表时，必须指定列")
                    extracted_results = []
                    for row in results:
                        extracted_row = [row[col] for col in columns]
                        extracted_results.extend(extracted_row) if len(columns) == 1 else extracted_results.append(
                            tuple(extracted_row))

                    return extracted_results

            except Exception as e:
                self.logger.error(f"数据库查询出错: {e}")
                return []

    def insert(self, table: str, values: Union[Dict[str, Any], List[Dict[str, Any]]]) -> int:
        # 统一转换为列表处理
        if isinstance(values, dict):
            values = [values]
        if not values:
            return 0

            # 检查所有字典的键是否一致，并排序确保字段顺序一致
        columns = sorted(values[0].keys())
        for v in values[1:]:
            if sorted(v.keys()) != columns:
                raise ValueError("所有字典的键必须一致")

        columns_str = ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(columns))
        sql = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"

        # 按排序后的列顺序提取值
        params = [tuple(v[col] for col in columns) for v in values]
        self.logger.info(f'INSERT_SQL: {sql}')

        # 记录参数日志
        formatted_params = [f"{value}({type(value).__name__})" for param in params for value in param]
        self.logger.info(f"PARAMS: {', '.join(formatted_params)}")

        with self.db_connection as conn:
            try:
                with conn.cursor() as cursor:
                    rows_affected = cursor.executemany(sql, params)
                conn.commit()
                self.logger.info(f"TOTAL: {rows_affected}")
                return rows_affected
            except Exception as e:
                conn.rollback()
                self.logger.error(f" 数据库插入出错: {e}")
                return -1

    def update(self, table: str, set_values: Dict[str, Any], conditions: Dict[str, Any]) -> int:
        set_clause = ', '.join([f"{k} = %s" for k in set_values.keys()])
        where_clause = ' AND '.join([f"{k} = %s" for k in conditions.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        params = tuple(set_values.values()) + tuple(conditions.values())
        self.logger.info(f'UPDATE_SQL: {sql}')
        formatted_params = [f"{v}({type(v).__name__})" for v in params]
        self.logger.info(f"PARAMS: {', '.join(formatted_params)}")

        with self.db_connection as conn:
            try:
                with conn.cursor() as cursor:
                    rows_affected = cursor.execute(sql, params)
                conn.commit()
                self.logger.info(f"TOTAL: {rows_affected}")
                return rows_affected
            except Exception as e:
                conn.rollback()
                self.logger.error(f"数据库更新出错: {e}")
                return -1

    def delete(self, table: str, conditions: Dict[str, Any]) -> int:
        where_clause = ' AND '.join([f"{k} = %s" for k in conditions.keys()])
        sql = f"DELETE FROM {table} WHERE {where_clause}"
        params = tuple(conditions.values())
        self.logger.info(f'DELETE_SQL: {sql}')
        formatted_params = [f"{v}({type(v).__name__})" for v in params]
        self.logger.info(f"params: {', '.join(formatted_params)}")

        with self.db_connection as conn:
            try:
                with conn.cursor() as cursor:
                    rows_affected = cursor.execute(sql, params)
                conn.commit()
                self.logger.info(f"rows_affected: {rows_affected}")
                return rows_affected
            except Exception as e:
                conn.rollback()
                self.logger.error(f"数据库删除出错: {e}")
                return -1

# 使用示例
if __name__ == "__main__":
    db_ops = MysqlOperations()
    # 查询数据
    # conditions = {"dmlb": "love", "dm": "01"}
    # columns = ["KC1"]
    results = db_ops.select("SEND_DM")

    now = datetime.now()
    #插入数据 Custom_Values = ["嫁你", "嫁给你", "像你", "娶我"]

    insert_values = {"CZSJ": now, "DM": "love_word", "DMLB": "love_quote","DMMC":'嫁给你',
                     'SYZT':1}
    affected_rows = db_ops.insert("SEND_DM", insert_values)


    # # 更新数据
    # set_values = {"dmlb": "love_quote"}
    # update_conditions = {"dmlb": 'love'}
    # db_ops.update("send_dm", set_values, update_conditions)


    # # 删除数据
    # delete_conditions = {"id": 7}
    # db_ops.delete("SEND_DM", delete_conditions)
