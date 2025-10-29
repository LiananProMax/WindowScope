"""
监视窗口 UI 组件 - 现代化版本
显示实时捕获的视频流
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QSlider, QGraphicsView, QGraphicsScene,
                             QWidget)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QPoint

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
    - 无边框现代设计
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
        
        # 拖拽相关
        self.dragging = False
        self.drag_position = QPoint()
        
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
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.Tool |
            Qt.WindowType.FramelessWindowHint
        )
        
        # 应用现代样式
        self.setStyleSheet("""
            QDialog {
                background-color: #0F172A;
                color: #F8FAFC;
                border: 2px solid #334155;
                border-radius: 8px;
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
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
        """)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
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
                border-bottom-left-radius: 6px;
                border-bottom-right-radius: 6px;
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
        self.scene.clear()
        self.scene.addPixmap(QPixmap.fromImage(image))
        
        # 更新场景和窗口尺寸
        width = image.width()
        height = image.height()
        self.view.setSceneRect(0, 0, width, height)
        
        # 自动调整窗口大小（仅首次）
        if self.engine.capture_count == 1:
            self.resize(width, height + 50)
    
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
    
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            logger.debug("开始拖拽监视窗口")
            event.accept()
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        if self.dragging:
            new_pos = event.globalPosition().toPoint() - self.drag_position
            self.move(new_pos)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        if self.dragging:
            logger.debug(f"拖拽结束，窗口位置: ({self.x()}, {self.y()})")
        self.dragging = False
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        logger.info(f"监视窗口关闭: '{self.window_title}'")
        self.engine.stop()
        event.accept()
