"""
WindowScope - 程序入口
"""
import sys
from PyQt6.QtWidgets import QApplication

from .config import settings
from .utils import logger
from .ui import MainWindow


def main():
    """主函数"""
    # 配置日志
    if settings.debug.log_to_file:
        logger.add_file_handler(settings.debug.log_file_path)
    
    # 打印启动信息
    logger.info("=" * 60)
    logger.info(f"🎥 {settings.app_name} v{settings.version} 启动")
    logger.info(f"Python 版本: {sys.version}")
    logger.info(f"调试模式: {'开启' if settings.debug.enabled else '关闭'}")
    logger.info(f"功能: 实时视频流监视，可调节帧率 ({settings.capture.min_fps}-{settings.capture.max_fps} FPS)")
    logger.info("=" * 60)
    
    # 创建应用程序
    app = QApplication(sys.argv)
    app.setApplicationName(settings.app_name)
    app.setApplicationVersion(settings.version)
    
    logger.info("PyQt6 应用程序已创建")
    
    # 创建并显示主窗口
    main_window = MainWindow()
    main_window.show()
    
    logger.info("主窗口已显示，等待用户选择窗口...\n")
    
    # 运行事件循环
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

