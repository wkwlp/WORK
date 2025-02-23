import os
import logging
import inspect
from colorlog import ColoredFormatter
from logging.handlers import RotatingFileHandler, SocketHandler


def setup_logger(level=logging.DEBUG):
    """
    配置同时输出到控制台(带颜色)和远程服务器的日志记录器

    Args:
        level (int): 日志级别，默认为logging.DEBUG

    Returns:
        logging.Logger: 配置好的日志记录器
    """
    # 获取调用者的完整文件路径
    caller_frame = inspect.stack()[1][0]
    caller_filename = inspect.getframeinfo(caller_frame).filename
    full_path = os.path.abspath(caller_filename)  # 获取完整路径

    # 定义仓库根路径
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # 仓库根路径是当前文件上一级目录

    # 获取相对于仓库根路径的相对路径
    relative_path = os.path.relpath(full_path, repo_root)

    # 将路径中的反斜杠 `\` 替换为点 `.`，并去掉文件扩展名
    module_style_path = relative_path.replace("\\", ".").replace("/", ".")
    module_style_path = module_style_path.replace(".py", "")  # 去掉 .py 后缀

    # 使用模块风格路径作为日志记录器的名称
    logger = logging.getLogger(module_style_path)
    logger.setLevel(level)

    # 如果已经存在处理器，则不再添加新的处理器
    if logger.hasHandlers():
        return logger

    console_format = (
        '%(log_color)s%(asctime)s [%(levelname)s] %(name)s.%(funcName)s:%(lineno)d - %(message)s'
    )
    colored_formatter = ColoredFormatter(
        console_format,
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'white',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(colored_formatter)
    logger.addHandler(console_handler)

    # ----------------- 网络处理器 -----------------
    try:
        host_port_str = os.getenv("HOST_PORT")
        if not host_port_str :
            logger.error("必须设置 HOST_PORT环境变量")
        host, port = host_port_str.split(':')
        tcp_handler = SocketHandler(
            host,int(port)
        )
        tcp_handler.setLevel(level)
        logger.addHandler(tcp_handler)
    except Exception as e:
        logger.error(f" 无法连接远程日志服务器: {str(e)}")

    return logger



# 示例调用代码
if __name__ == "__main__":
    def some_function():
        logger = setup_logger()

        # 记录不同级别的日志
        logger.debug("这是一个调试信息")
        logger.info("这是一个信息消息")
        logger.warning("这是一个警告信息")
        logger.error("这是一个错误信息")
        logger.critical("这是一个严重错误信息")

    some_function()

