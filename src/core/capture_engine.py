"""
捕获引擎模块
负责实时捕获窗口内容
"""
import time
from typing import Optional, Tuple, Callable
from PyQt6.QtCore import QTimer, QObject, pyqtSignal
from PyQt6.QtGui import QImage

from ..utils import logger, ScreenCapture, WindowManager
from ..config import settings


class CaptureEngine(QObject):
    """
    捕获引擎类
    
    职责：
    - 管理捕获定时器
    - 执行实际的屏幕捕获
    - 计算 FPS
    - 发射捕获事件
    """
    
    # 信号定义
    frame_captured = pyqtSignal(QImage)  # 捕获到新帧
    capture_failed = pyqtSignal(str)      # 捕获失败
    fps_updated = pyqtSignal(float)       # FPS 更新
    method_changed = pyqtSignal(str)      # 捕获方法变更
    
    def __init__(self, hwnd: int, region: Tuple[int, int, int, int], fps: int = 30):
        """
        初始化捕获引擎
        
        Args:
            hwnd: 目标窗口句柄
            region: 捕获区域 (x, y, width, height)
            fps: 目标帧率
        """
        super().__init__()
        
        self.hwnd = hwnd
        self.region = region
        self.fps = fps
        
        # 状态
        self.is_running = False
        self.is_paused = False
        self.capture_count = 0
        self.failed_count = 0
        self.current_method = ""
        
        # FPS 计算
        self.frame_times = []
        self.actual_fps = 0.0
        
        # 定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self._capture_frame)
        
        logger.info(f"捕获引擎已初始化: hwnd={hwnd}, region={region}, fps={fps}")
    
    def start(self):
        """启动捕获"""
        if not self.is_running:
            self.is_running = True
            self.is_paused = False
            interval_ms = int(1000 / self.fps)
            self.timer.start(interval_ms)
            logger.info(f"捕获引擎已启动，刷新间隔: {interval_ms}ms ({self.fps} FPS)")
    
    def stop(self):
        """停止捕获"""
        if self.is_running:
            self.is_running = False
            self.timer.stop()
            logger.info("捕获引擎已停止")
    
    def pause(self):
        """暂停捕获"""
        if self.is_running and not self.is_paused:
            self.is_paused = True
            self.timer.stop()
            logger.info("捕获已暂停")
    
    def resume(self):
        """恢复捕获"""
        if self.is_running and self.is_paused:
            self.is_paused = False
            interval_ms = int(1000 / self.fps)
            self.timer.start(interval_ms)
            logger.info(f"捕获已恢复，刷新间隔: {interval_ms}ms")
    
    def set_fps(self, fps: int):
        """
        设置帧率
        
        Args:
            fps: 新的帧率
        """
        if settings.capture.min_fps <= fps <= settings.capture.max_fps:
            self.fps = fps
            if self.is_running and not self.is_paused:
                interval_ms = int(1000 / fps)
                self.timer.stop()
                self.timer.start(interval_ms)
                logger.info(f"帧率已调整为: {fps} FPS ({interval_ms}ms)")
    
    def _capture_frame(self):
        """捕获一帧（内部方法）"""
        try:
            self.capture_count += 1
            verbose = (self.capture_count % settings.debug.verbose_interval == 1)
            
            if verbose:
                logger.debug(f"--- 第 {self.capture_count} 帧 ---")
            
            # 获取窗口尺寸
            rect = WindowManager.get_window_rect(self.hwnd)
            window_width = rect[2] - rect[0]
            window_height = rect[3] - rect[1]
            
            if window_width <= 0 or window_height <= 0:
                if verbose:
                    logger.warning(f"窗口尺寸无效: {window_width}x{window_height}")
                self.failed_count += 1
                return
            
            # 捕获窗口
            img, method = ScreenCapture.capture_window(self.hwnd, window_width, window_height)
            
            if img is None or img.isNull():
                self.failed_count += 1
                if verbose:
                    logger.warning(f"捕获失败 (失败计数: {self.failed_count})")
                
                if self.failed_count > 5:
                    # 检查窗口是否被最小化
                    if WindowManager.is_window_minimized(self.hwnd):
                        self.capture_failed.emit("目标窗口已最小化，无法捕获内容。请恢复窗口！")
                        logger.warning("捕获失败：窗口已最小化")
                    else:
                        self.capture_failed.emit("连续捕获失败，请检查目标窗口状态")
                return
            
            # 捕获成功，重置失败计数
            self.failed_count = 0
            
            # 记录捕获方法变更
            if method != self.current_method:
                self.current_method = method
                self.method_changed.emit(method)
                logger.info(f"捕获方法: {method}")
            
            # 裁剪图像
            x, y, width, height = self.region
            x = max(0, min(x, window_width - 1))
            y = max(0, min(y, window_height - 1))
            width = min(width, window_width - x)
            height = min(height, window_height - y)
            
            cropped_img = img.copy(x, y, width, height)
            
            # 发射信号
            self.frame_captured.emit(cropped_img)
            
            # 计算 FPS
            self._calculate_fps()
            
            if verbose:
                logger.debug(f"✓ 第 {self.capture_count} 帧完成 "
                           f"(方法: {self.current_method}, FPS: {self.actual_fps:.1f})")
            
        except Exception as e:
            logger.error(f"捕获帧时发生错误: {e}")
            self.capture_failed.emit(str(e))
    
    def _calculate_fps(self):
        """计算实际 FPS"""
        current_time = time.time()
        self.frame_times.append(current_time)
        
        # 只保留最近 1 秒的帧时间
        self.frame_times = [t for t in self.frame_times if current_time - t <= 1.0]
        
        if len(self.frame_times) > 1:
            self.actual_fps = len(self.frame_times)
            self.fps_updated.emit(self.actual_fps)

