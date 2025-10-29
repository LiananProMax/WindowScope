"""
日志管理模块
提供统一的日志记录功能
"""
import logging
import sys
from pathlib import Path
from typing import Optional


class Logger:
    """日志管理器"""
    
    _instance: Optional['Logger'] = None
    _logger: Optional[logging.Logger] = None
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """初始化日志器"""
        if self._logger is None:
            self._setup_logger()
    
    def _setup_logger(self):
        """设置日志器"""
        self._logger = logging.getLogger('WindowCapture')
        self._logger.setLevel(logging.DEBUG)
        
        # 控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        
        # 格式化器
        formatter = logging.Formatter(
            '[%(levelname)s] %(message)s'
        )
        console_handler.setFormatter(formatter)
        
        self._logger.addHandler(console_handler)
    
    def add_file_handler(self, log_file: str):
        """添加文件处理器"""
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            '%(asctime)s - [%(levelname)s] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        
        self._logger.addHandler(file_handler)
    
    def debug(self, message: str):
        """调试信息"""
        if self._logger:
            self._logger.debug(message)
    
    def info(self, message: str):
        """一般信息"""
        if self._logger:
            self._logger.info(message)
    
    def warning(self, message: str):
        """警告信息"""
        if self._logger:
            self._logger.warning(message)
    
    def error(self, message: str):
        """错误信息"""
        if self._logger:
            self._logger.error(message)
    
    def critical(self, message: str):
        """严重错误"""
        if self._logger:
            self._logger.critical(message)


# 全局日志实例
logger = Logger()

