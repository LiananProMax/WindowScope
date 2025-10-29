"""
配置管理模块
集中管理应用程序的所有配置项
"""
from dataclasses import dataclass
from typing import Tuple


@dataclass
class CaptureSettings:
    """捕获设置"""
    default_fps: int = 30
    min_fps: int = 1
    max_fps: int = 60
    min_region_size: int = 10  # 最小选择区域尺寸
    

@dataclass
class UISettings:
    """界面设置"""
    main_window_width: int = 450
    main_window_height: int = 350
    main_window_x: int = 100
    main_window_y: int = 100
    
    # 区域选择器设置
    selector_max_width: int = 1200
    selector_max_height: int = 800
    
    # 控制栏高度
    control_bar_height: int = 50


@dataclass
class DebugSettings:
    """调试设置"""
    enabled: bool = True
    verbose_interval: int = 30  # 每N帧输出一次详细信息
    log_to_file: bool = False
    log_file_path: str = "window_capture.log"


@dataclass
class AppSettings:
    """应用程序总配置"""
    app_name: str = "WindowScope"
    version: str = "2.1.0"
    
    capture: CaptureSettings = None
    ui: UISettings = None
    debug: DebugSettings = None
    
    def __post_init__(self):
        """初始化后处理"""
        if self.capture is None:
            self.capture = CaptureSettings()
        if self.ui is None:
            self.ui = UISettings()
        if self.debug is None:
            self.debug = DebugSettings()


# 全局配置实例
settings = AppSettings()

