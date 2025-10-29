"""
监视窗口 UI 组件 - 现代化版本
显示实时捕获的视频流
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QSlider, QGraphicsView, QGraphicsScene,
                             QWidget, QApplication)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QPoint, QRectF

from ..core import CaptureEngine
from ..config import settings
from ..utils import logger


class CaptureWindow(QDialog):
    """
    现代化监视窗口
    
    改进项：
    - 时尚的深色界面
    - 增强的控制栏设计
    - 实时性能指标
    - 可调整窗口大小
    - 等比例缩放视频内容
    - 窗口置顶，易于拖动和调整
    """
    
    def __init__(self, engine: CaptureEngine, window_title: str, parent=None):
        """
        初始化监视窗口
        
        Args:
            engine: 捕获引擎实例
            window_title: 窗口标题
            parent: 父窗口
        """
        super().__init__(parent)
        
        self.engine = engine
        self.window_title = window_title
        
        # 视频原始尺寸（用于等比例缩放）
        self.original_width = 0
        self.original_height = 0
        self.current_pixmap = None
        
        # 连接信号
        self._connect_signals()
        
        # 初始化 UI
        self._init_ui()
        
        logger.info(f"现代化监视窗口已创建: '{window_title}'")
    
    def _connect_signals(self):
        """连接捕获引擎的信号"""
        self.engine.frame_captured.connect(self.on_frame_captured)
        self.engine.fps_updated.connect(self.on_fps_updated)
        self.engine.method_changed.connect(self.on_method_changed)
        self.engine.capture_failed.connect(self.on_capture_failed)
    
    def _init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle(f"📺 监视: {self.window_title}")
        # 保持置顶，但使用正常窗口边框（允许用户调整大小）
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint
        )
        
        # 设置初始窗口大小（避免窗口太小看不见）
        self.resize(800, 600)
        
        # 将窗口移到屏幕中心
        screen = QApplication.primaryScreen().availableGeometry()
        screen_center_x = screen.x() + (screen.width() - 800) // 2
        screen_center_y = screen.y() + (screen.height() - 600) // 2
        self.move(screen_center_x, screen_center_y)
        
        logger.info(f"监视窗口初始化: 初始大小 800x600, 位置 ({screen_center_x}, {screen_center_y})")
        
        # 应用现代样式
        self.setStyleSheet("""
            QDialog {
                background-color: #0F172A;
                color: #F8FAFC;
            }
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 图形视图
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setStyleSheet("""
            QGraphicsView {
                background: #0F172A;
                border: none;
            }
        """)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # 设置等比例缩放模式
        self.view.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)
        self.view.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)
        
        main_layout.addWidget(self.view)
        
        # 控制栏
        control_layout = self._create_control_bar()
        main_layout.addLayout(control_layout)
        
        self.setLayout(main_layout)
    
    def _create_control_bar(self) -> QHBoxLayout:
        """创建现代化控制栏"""
        # 控制栏容器
        container = QHBoxLayout()
        container.setContentsMargins(0, 0, 0, 0)
        container.setSpacing(0)
        
        # 创建控制栏 widget
        control_widget = QWidget()
        control_widget.setStyleSheet("""
            QWidget {
                background-color: #1E293B;
                border-top: 1px solid #334155;
            }
        """)
        
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(8, 8, 8, 8)
        control_layout.setSpacing(8)
        
        # 暂停/继续按钮
        self.pause_btn = QPushButton("⏸")
        self.pause_btn.setFixedSize(32, 32)
        self.pause_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
        """)
        self.pause_btn.clicked.connect(self.toggle_pause)
        control_layout.addWidget(self.pause_btn)
        
        # FPS 显示
        self.fps_label = QLabel(f"FPS: {self.engine.fps}")
        self.fps_label.setStyleSheet("""
            QLabel {
                color: #10B981;
                font-weight: 700;
                font-size: 11px;
                min-width: 50px;
            }
        """)
        control_layout.addWidget(self.fps_label)
        
        # 分割线
        divider1 = QLabel("│")
        divider1.setStyleSheet("color: #334155; margin: 0 4px;")
        control_layout.addWidget(divider1)
        
        # FPS 调节图标
        fps_icon = QLabel("📊")
        control_layout.addWidget(fps_icon)
        
        # FPS 滑块
        self.fps_slider = QSlider(Qt.Orientation.Horizontal)
        self.fps_slider.setMinimum(settings.capture.min_fps)
        self.fps_slider.setMaximum(settings.capture.max_fps)
        self.fps_slider.setValue(self.engine.fps)
        self.fps_slider.setFixedWidth(120)
        self.fps_slider.valueChanged.connect(self.on_fps_slider_changed)
        control_layout.addWidget(self.fps_slider)
        
        # FPS 数值
        self.fps_value_label = QLabel(f"{self.engine.fps}")
        self.fps_value_label.setFixedWidth(30)
        self.fps_value_label.setStyleSheet("color: #94A3B8; font-size: 10px;")
        control_layout.addWidget(self.fps_value_label)
        
        control_layout.addSpacing(8)
        
        # 分割线
        divider2 = QLabel("│")
        divider2.setStyleSheet("color: #334155; margin: 0 4px;")
        control_layout.addWidget(divider2)
        
        # 状态标签
        self.status_label = QLabel("🟢")
        self.status_label.setStyleSheet("font-size: 12px;")
        control_layout.addWidget(self.status_label)
        
        # 方法标签
        self.method_label = QLabel("检测中...")
        self.method_label.setStyleSheet("""
            QLabel {
                color: #94A3B8;
                font-size: 9px;
                margin-left: 4px;
            }
        """)
        control_layout.addWidget(self.method_label)
        
        control_layout.addStretch()
        
        # 关闭按钮
        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(32, 32)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #EF4444;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
                font-weight: 700;
            }
            QPushButton:hover {
                background-color: #DC2626;
            }
        """)
        self.close_btn.clicked.connect(self.close)
        control_layout.addWidget(self.close_btn)
        
        control_widget.setLayout(control_layout)
        container.addWidget(control_widget)
        
        return container
    
    def on_frame_captured(self, image: QImage):
        """
        处理捕获到的帧
        
        Args:
            image: 捕获的图像
        """
        # 保存原始尺寸和图像
        if self.original_width == 0:
            self.original_width = image.width()
            self.original_height = image.height()
            logger.info(f"视频原始尺寸: {self.original_width}x{self.original_height}")
        
        self.current_pixmap = QPixmap.fromImage(image)
        
        # 更新场景
        self.scene.clear()
        self.scene.addPixmap(self.current_pixmap)
        self.view.setSceneRect(0, 0, image.width(), image.height())
        
        # 自动调整窗口大小（仅首次）
        if self.engine.capture_count == 1:
            self._set_initial_size(image.width(), image.height())
            self._fit_in_view()
    
    def on_fps_updated(self, fps: float):
        """
        FPS 更新回调
        
        Args:
            fps: 实际 FPS
        """
        self.fps_label.setText(f"FPS: {fps:.1f}")
    
    def on_method_changed(self, method: str):
        """
        捕获方法变更回调
        
        Args:
            method: 捕获方法名称
        """
        self.method_label.setText(f"{method}")
        logger.info(f"捕获方法: {method}")
    
    def on_capture_failed(self, error_message: str):
        """
        捕获失败回调
        
        Args:
            error_message: 错误信息
        """
        self.status_label.setText("❌")
        self.method_label.setText("错误")
        logger.error(f"捕获失败: {error_message}")
    
    def toggle_pause(self):
        """切换暂停/继续状态"""
        if self.engine.is_paused:
            self.engine.resume()
            self.pause_btn.setText("⏸")
            self.status_label.setText("🟢")
        else:
            self.engine.pause()
            self.pause_btn.setText("▶")
            self.status_label.setText("⏸")
    
    def on_fps_slider_changed(self, value: int):
        """
        帧率滑块改变回调
        
        Args:
            value: 新的帧率值
        """
        self.fps_value_label.setText(str(value))
        self.engine.set_fps(value)
    
    def _set_initial_size(self, video_width: int, video_height: int):
        """
        设置窗口初始大小，限制在屏幕范围内
        
        Args:
            video_width: 视频宽度
            video_height: 视频高度
        """
        # 获取屏幕可用区域
        screen = QApplication.primaryScreen().availableGeometry()
        screen_width = screen.width()
        screen_height = screen.height()
        
        # 控制栏高度
        control_height = 50
        
        # 计算最大可用尺寸（留出边距）
        max_width = int(screen_width * 0.8)  # 屏幕宽度的80%
        max_height = int(screen_height * 0.8) - control_height  # 屏幕高度的80%减去控制栏
        
        # 计算缩放比例，保持宽高比
        scale = min(
            max_width / video_width,
            max_height / video_height,
            1.0  # 如果视频小于最大尺寸，不放大
        )
        
        # 计算窗口尺寸
        window_width = int(video_width * scale)
        window_height = int(video_height * scale) + control_height
        
        logger.info(f"窗口初始大小: {window_width}x{window_height} (缩放比例: {scale:.2f})")
        
        # 设置窗口大小
        self.resize(window_width, window_height)
        
        # 将窗口移到屏幕中心
        window_x = screen.x() + (screen_width - window_width) // 2
        window_y = screen.y() + (screen_height - window_height) // 2
        self.move(window_x, window_y)
        
        logger.info(f"窗口位置: ({window_x}, {window_y})")
    
    def _fit_in_view(self):
        """等比例缩放视频以适应窗口"""
        if self.current_pixmap and not self.current_pixmap.isNull():
            # 等比例缩放，保持宽高比
            self.view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
    
    def resizeEvent(self, event):
        """窗口大小改变事件"""
        super().resizeEvent(event)
        # 窗口大小改变时，重新等比例缩放视频
        self._fit_in_view()
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        logger.info(f"监视窗口关闭: '{self.window_title}'")
        self.engine.stop()
        event.accept()
