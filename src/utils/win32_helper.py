"""
Windows API 辅助工具
封装常用的 Windows API 调用
"""
import ctypes
import win32gui
import win32con
import win32ui
from ctypes import windll
from typing import List, Tuple, Optional
from PyQt6.QtGui import QImage

from .logger import logger


class BITMAPINFOHEADER(ctypes.Structure):
    """位图信息头结构"""
    _fields_ = [
        ("biSize", ctypes.c_uint32),
        ("biWidth", ctypes.c_int32),
        ("biHeight", ctypes.c_int32),
        ("biPlanes", ctypes.c_uint16),
        ("biBitCount", ctypes.c_uint16),
        ("biCompression", ctypes.c_uint32),
        ("biSizeImage", ctypes.c_uint32),
        ("biXPelsPerMeter", ctypes.c_int32),
        ("biYPelsPerMeter", ctypes.c_int32),
        ("biClrUsed", ctypes.c_uint32),
        ("biClrImportant", ctypes.c_uint32)
    ]


class BITMAPINFO(ctypes.Structure):
    """位图信息结构"""
    _fields_ = [
        ("bmiHeader", BITMAPINFOHEADER),
        ("bmiColors", ctypes.c_uint32 * 3)
    ]


class WindowManager:
    """Windows 窗口管理器"""
    
    @staticmethod
    def enum_windows() -> List[Tuple[int, str]]:
        """
        枚举所有可见窗口
        
        Returns:
            List[Tuple[hwnd, title]]: 窗口句柄和标题列表
        """
        logger.debug("开始枚举窗口...")
        windows = []
        
        def callback(hwnd, windows_list):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title:
                    windows_list.append((hwnd, title))
                    logger.debug(f"  找到窗口: HWND={hwnd}, 标题='{title}'")
        
        win32gui.EnumWindows(callback, windows)
        logger.debug(f"窗口枚举完成，共找到 {len(windows)} 个窗口")
        return windows
    
    @staticmethod
    def get_window_rect(hwnd: int) -> Tuple[int, int, int, int]:
        """获取窗口矩形区域"""
        return win32gui.GetWindowRect(hwnd)
    
    @staticmethod
    def get_window_title(hwnd: int) -> str:
        """获取窗口标题"""
        return win32gui.GetWindowText(hwnd)


class CaptureMethod:
    """屏幕捕获方法枚举"""
    WIN32UI = "win32ui"
    PRINT_WINDOW = "PrintWindow"
    BITBLT = "BitBlt"


class ScreenCapture:
    """屏幕捕获工具"""
    
    @staticmethod
    def capture_window_win32ui(hwnd: int, width: int, height: int) -> Tuple[Optional[QImage], bool]:
        """
        使用 win32ui 方法捕获窗口
        
        Args:
            hwnd: 窗口句柄
            width: 窗口宽度
            height: 窗口高度
            
        Returns:
            Tuple[QImage, success]: 图像和成功标志
        """
        try:
            hwndDC = win32gui.GetWindowDC(hwnd)
            mfcDC = win32ui.CreateDCFromHandle(hwndDC)
            saveDC = mfcDC.CreateCompatibleDC()
            
            saveBitMap = win32ui.CreateBitmap()
            saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
            saveDC.SelectObject(saveBitMap)
            
            # 尝试 PrintWindow
            result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)
            
            # 如果失败，尝试 BitBlt
            if not result:
                result = saveDC.BitBlt((0, 0), (width, height), 
                                      mfcDC, (0, 0), win32con.SRCCOPY)
            
            # 获取位图数据
            bmpstr = saveBitMap.GetBitmapBits(True)
            img = QImage(bmpstr, width, height, QImage.Format.Format_RGB32)
            
            # 清理资源
            win32gui.DeleteObject(saveBitMap.GetHandle())
            saveDC.DeleteDC()
            mfcDC.DeleteDC()
            win32gui.ReleaseDC(hwnd, hwndDC)
            
            return img, True
            
        except Exception as e:
            logger.error(f"win32ui 捕获失败: {e}")
            return None, False
    
    @staticmethod
    def capture_window_printwindow(hwnd: int, width: int, height: int) -> Tuple[Optional[QImage], bool]:
        """
        使用 PrintWindow API 捕获窗口
        
        Args:
            hwnd: 窗口句柄
            width: 窗口宽度
            height: 窗口高度
            
        Returns:
            Tuple[QImage, success]: 图像和成功标志
        """
        try:
            hwndDC = win32gui.GetWindowDC(hwnd)
            mfcDC = win32gui.CreateCompatibleDC(hwndDC)
            saveBitMap = win32gui.CreateCompatibleBitmap(hwndDC, width, height)
            win32gui.SelectObject(mfcDC, saveBitMap)
            
            # PrintWindow 截图
            print_result = windll.user32.PrintWindow(hwnd, mfcDC, 2)
            
            if not print_result:
                # 清理并返回失败
                win32gui.DeleteObject(saveBitMap)
                win32gui.DeleteDC(mfcDC)
                win32gui.ReleaseDC(hwnd, hwndDC)
                return None, False
            
            # 定义BITMAPINFO
            bmpinfo = BITMAPINFO()
            bmpinfo.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
            bmpinfo.bmiHeader.biWidth = width
            bmpinfo.bmiHeader.biHeight = -height
            bmpinfo.bmiHeader.biPlanes = 1
            bmpinfo.bmiHeader.biBitCount = 32
            bmpinfo.bmiHeader.biCompression = win32con.BI_RGB
            
            buf_len = width * height * 4
            buffer = (ctypes.c_char * buf_len)()
            
            hbitmap_int = int(saveBitMap)
            mfcDC_int = int(mfcDC)
            
            dibits_result = windll.gdi32.GetDIBits(
                mfcDC_int, hbitmap_int, 0, height,
                ctypes.byref(buffer), ctypes.byref(bmpinfo),
                win32con.DIB_RGB_COLORS
            )
            
            # 清理资源
            win32gui.DeleteObject(saveBitMap)
            win32gui.DeleteDC(mfcDC)
            win32gui.ReleaseDC(hwnd, hwndDC)
            
            if dibits_result == 0:
                return None, False
            
            img = QImage(buffer, width, height, QImage.Format.Format_ARGB32)
            return img, True
            
        except Exception as e:
            logger.error(f"PrintWindow 捕获失败: {e}")
            return None, False
    
    @classmethod
    def capture_window(cls, hwnd: int, width: int, height: int) -> Tuple[Optional[QImage], str]:
        """
        捕获窗口（自动尝试多种方法）
        
        Args:
            hwnd: 窗口句柄
            width: 窗口宽度
            height: 窗口高度
            
        Returns:
            Tuple[QImage, method]: 图像和使用的方法名称
        """
        # 方法1: 优先使用 win32ui
        img, success = cls.capture_window_win32ui(hwnd, width, height)
        if success:
            return img, CaptureMethod.WIN32UI
        
        # 方法2: 如果失败，尝试 PrintWindow
        img, success = cls.capture_window_printwindow(hwnd, width, height)
        if success:
            return img, CaptureMethod.PRINT_WINDOW
        
        return None, ""

