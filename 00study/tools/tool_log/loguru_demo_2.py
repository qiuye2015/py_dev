import os
import threading

from loguru import logger

# 定义日志格式，包括进程名和线程名
log_format = (
    "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
    "P:{process} ({process.name}) | "  # 显示进程ID和进程名
    "T:{thread} ({thread.name}) | "  # 显示线程ID和线程名
    "{level: <8} | "
    "{message}"
)

# 配置logger
logger.configure(handlers=[{"sink": "your_log_file.log", "format": log_format}])

# 示例日志记录
logger.debug("This is a debug message.")
logger.info(f"Current process name: {os.getpid()} ({os.getpid()})")
logger.info(f"Current thread name: {threading.current_thread().ident} ({threading.current_thread().name})")
