"""
区域选择器 UI 组件 - 现代化版本
提供图形化的区域选择界面
"""
from PyQt6.QtWidgets import (QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout)
from PyQt6.QtGui import QPixmap, QImage, QPainter, QColor, QPen, QBrush, QCursor
from PyQt6.QtCore import Qt, QPoint, QRect

from ..config import settings
from ..utils import logger


class RegionSelector(QDialog):
    """
    现代化区域选择器
    
    改进项：
    - 深色主题界面
    - 翠绿色选择框
    - 优化的视觉反馈
    - 清晰的操作提示
    """
    
    def __init__(self, screenshot: QImage, window_width: int, window_height: int, parent=None):
        """
        初始化区域选择器
        
        Args:
            screenshot: 窗口截图
            window_width: 窗口宽度
            window_height: 窗口高度
            parent: 父窗口
        """
        super().__init__(parent)
        
        self.screenshot = screenshot
        self.window_width = window_width
        self.window_height = window_height
        self.selected_rect = None
        
        # 选择状态
        self.selecting = False
        self.start_point = QPoint()
        self.end_point = QPoint()
        self.current_rect = QRect()
        
        self._init_ui()
        
        logger.debug(f"现代化区域选择器已创建: {window_width}x{window_height}")
    
    def _init_ui(self):
        """初始化 UI"""
        self.setWindowTitle("📐 拖拽选择监视区域")
        self.setModal(True)
        
        # 应用深色主题
        self.setStyleSheet("""
            QDialog {
                background-color: #0F172A;
                color: #F8FAFC;
            }
            QPushButton {
                background-color: #2563EB;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 600;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
            QPushButton#cancelBtn {
                background-color: #6B7280;
            }
            QPushButton#cancelBtn:hover {
                background-color: #4B5563;
            }
            QPushButton#confirmBtn {
                background-color: #10B981;
            }
            QPushButton#confirmBtn:hover {
                background-color: #059669;
            }
            QPushButton:disabled {
                background-color: #374151;
                color: #6B7280;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 信息栏
        info_layout = QHBoxLayout()
        info_layout.setContentsMargins(16, 12, 16, 12)
        info_layout.setSpacing(12)
        
        tip_label = QLabel("💡 在图片上拖拽鼠标选择要监视的区域")
        tip_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-weight: 600;
                color: #06B6D4;
            }
        """)
        info_layout.addWidget(tip_label)
        
        self.coord_label = QLabel("等待选择...")
        self.coord_label.setStyleSheet("""
            QLabel {
                font-size: 11px;
                color: #94A3B8;
            }
        """)
        info_layout.addWidget(self.coord_label)
        info_layout.addStretch()
        
        layout.addLayout(info_layout)
        
        # 分割线
        divider = QLabel()
        divider.setStyleSheet("background-color: #334155;")
        divider.setFixedHeight(1)
        layout.addWidget(divider)
        
        # 计算缩放比例
        ui_cfg = settings.ui
        scale = min(
            ui_cfg.selector_max_width / self.window_width,
            ui_cfg.selector_max_height / self.window_height,
            1.0
        )
        self.scale = scale
        
        display_width = int(self.window_width * scale)
        display_height = int(self.window_height * scale)
        
        logger.debug(f"区域选择器缩放: {scale:.2f}, 显示尺寸: {display_width}x{display_height}")
        
        # 图片显示标签
        self.image_label = QLabel()
        self.image_label.setMouseTracking(True)
        self.image_label.setCursor(QCursor(Qt.CursorShape.CrossCursor))
        self.image_label.setStyleSheet("background-color: #000000;")
        
        self._update_display()
        layout.addWidget(self.image_label, 0, Qt.AlignmentFlag.AlignCenter)
        
        # 分割线
        divider2 = QLabel()
        divider2.setStyleSheet("background-color: #334155;")
        divider2.setFixedHeight(1)
        layout.addWidget(divider2)
        
        # 按钮栏
        button_layout = self._create_button_bar()
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.resize(display_width + 24, display_height + 140)
    
    def _create_button_bar(self) -> QHBoxLayout:
        """创建按钮栏"""
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(16, 12, 16, 12)
        button_layout.setSpacing(8)
        
        # 全选按钮
        self.full_btn = QPushButton("📺 选择整个窗口")
        self.full_btn.clicked.connect(self._select_full_window)
        button_layout.addWidget(self.full_btn)
        
        # 重置按钮
        self.reset_btn = QPushButton("🔄 重新选择")
        self.reset_btn.clicked.connect(self._reset_selection)
        button_layout.addWidget(self.reset_btn)
        
        button_layout.addStretch()
        
        # 取消按钮
        self.cancel_btn = QPushButton("❌ 取消")
        self.cancel_btn.setObjectName("cancelBtn")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        # 确认按钮
        self.confirm_btn = QPushButton("✅ 确认选择")
        self.confirm_btn.setObjectName("confirmBtn")
        self.confirm_btn.setEnabled(False)
        self.confirm_btn.clicked.connect(self.accept)
        button_layout.addWidget(self.confirm_btn)
        
        return button_layout
    
    def _update_display(self):
        """更新显示的图片（带选择框）"""
        display_image = self.screenshot.copy()
        
        if not self.current_rect.isNull():
            painter = QPainter(display_image)
            
            # 绘制半透明蒙版（未选中区域）
            painter.fillRect(0, 0, self.window_width, self.window_height, 
                           QColor(0, 0, 0, 120))
            
            # 清除选中区域的蒙版
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
            painter.fillRect(self.current_rect, QColor(0, 0, 0, 0))
            
            # 绘制选择框边框（翠绿色）
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
            pen = QPen(QColor(16, 185, 129), 3, Qt.PenStyle.SolidLine)
            painter.setPen(pen)
            painter.drawRect(self.current_rect)
            
            # 绘制角点
            corner_size = 10
            painter.setBrush(QBrush(QColor(16, 185, 129)))
            corners = [
                self.current_rect.topLeft(),
                self.current_rect.topRight(),
                self.current_rect.bottomLeft(),
                self.current_rect.bottomRight()
            ]
            for corner in corners:
                painter.drawEllipse(
                    corner.x() - corner_size//2,
                    corner.y() - corner_size//2,
                    corner_size, corner_size
                )
            
            painter.end()
        
        # 缩放显示
        scaled_pixmap = QPixmap.fromImage(display_image).scaled(
            int(self.window_width * self.scale),
            int(self.window_height * self.scale),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        
        self.image_label.setPixmap(scaled_pixmap)
    
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            # 转换坐标到原始图片坐标
            pos = self.image_label.mapFrom(self, event.pos())
            actual_x = int(pos.x() / self.scale)
            actual_y = int(pos.y() / self.scale)
            
            if 0 <= actual_x < self.window_width and 0 <= actual_y < self.window_height:
                self.selecting = True
                self.start_point = QPoint(actual_x, actual_y)
                self.end_point = self.start_point
                self.current_rect = QRect(self.start_point, self.end_point)
                self._update_display()
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        if self.selecting:
            pos = self.image_label.mapFrom(self, event.pos())
            actual_x = int(pos.x() / self.scale)
            actual_y = int(pos.y() / self.scale)
            
            # 限制在图片范围内
            actual_x = max(0, min(actual_x, self.window_width - 1))
            actual_y = max(0, min(actual_y, self.window_height - 1))
            
            self.end_point = QPoint(actual_x, actual_y)
            self.current_rect = QRect(self.start_point, self.end_point).normalized()
            
            self._update_coord_label()
            self._update_display()
    
    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        if event.button() == Qt.MouseButton.LeftButton and self.selecting:
            self.selecting = False
            
            min_size = settings.capture.min_region_size
            if self.current_rect.width() > min_size and self.current_rect.height() > min_size:
                self.selected_rect = self.current_rect
                self.confirm_btn.setEnabled(True)
                self._update_coord_label()
                logger.debug(f"区域已选择: x={self.current_rect.x()}, y={self.current_rect.y()}, "
                          f"w={self.current_rect.width()}, h={self.current_rect.height()}")
            else:
                self._reset_selection()
    
    def _update_coord_label(self):
        """更新坐标标签"""
        if not self.current_rect.isNull():
            self.coord_label.setText(
                f"X={self.current_rect.x()}, Y={self.current_rect.y()}, "
                f"宽={self.current_rect.width()}, 高={self.current_rect.height()}"
            )
            self.coord_label.setStyleSheet("""
                QLabel {
                    font-size: 11px;
                    color: #10B981;
                    font-weight: 600;
                }
            """)
        else:
            self.coord_label.setText("等待选择...")
            self.coord_label.setStyleSheet("""
                QLabel {
                    font-size: 11px;
                    color: #94A3B8;
                }
            """)
    
    def _select_full_window(self):
        """选择整个窗口"""
        self.current_rect = QRect(0, 0, self.window_width, self.window_height)
        self.selected_rect = self.current_rect
        self.confirm_btn.setEnabled(True)
        self._update_coord_label()
        self._update_display()
        logger.debug("已选择整个窗口")
    
    def _reset_selection(self):
        """重置选择"""
        self.current_rect = QRect()
        self.selected_rect = None
        self.confirm_btn.setEnabled(False)
        self._update_coord_label()
        self._update_display()
        logger.debug("选择已重置")
    
    def get_selected_region(self):
        """获取选择的区域"""
        if self.selected_rect:
            return (self.selected_rect.x(), self.selected_rect.y(),
                   self.selected_rect.width(), self.selected_rect.height())
        return None
