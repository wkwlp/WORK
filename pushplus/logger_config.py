import logging
import inspect
import os
from colorlog import ColoredFormatter

def setup_logger(level=logging.INFO):
    """
    配置并返回一个只输出到控制台且带有颜色的日志记录器。

    Args:
        level (int): 日志级别，默认为logging.INFO。

    Returns:
        logging.Logger: 配置好的日志记录器。
    """
    # 获取调用者的完整文件路径
    caller_frame = inspect.stack()[1][0]
    caller_filename = inspect.getframeinfo(caller_frame).filename
    full_path = os.path.abspath(caller_filename)  # 获取完整路径

    # 定义仓库根路径
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # 仓库根路径是当前文的上一级目录


    # 获取相对于仓库根路径的相对路径
    relative_path = os.path.relpath(full_path, repo_root)

    # 将路径中的反斜杠 `\` 替换为点 `.`，并去掉文件扩展名
    module_style_path = relative_path.replace("\\", ".").replace("/", ".")

    # 使用模块风格路径作为日志记录器的名称
    logger = logging.getLogger(module_style_path)
    logger.setLevel(level)

    # 如果已经存在处理器，则不再添加新的处理器
    if logger.hasHandlers():
        return logger

    # 设置日志格式，包含时间、日志级别、模块风格路径、行号和消息
    log_format = '%(log_color)s%(asctime)s - %(name)s - %(levelname)s [%(filename)s:%(lineno)d] - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'

    # 创建彩色日志格式器
    colored_formatter = ColoredFormatter(
        log_format,
        datefmt=date_format,
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )

    # 创建控制台处理器并设置格式
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(colored_formatter)

    # 添加处理器到记录器
    logger.addHandler(console_handler)

    return logger