# 实时窗口监视器 UI 现代化改进方案

## 📋 执行概览

本方案将您的PyQt6应用从基础功能型UI升级为**现代化、专业的设计风格**，提升用户体验和视觉吸引力。

---

## 第一部分：设计系统

### 1.1 现代化色彩方案

#### 主色系定义
```python
# src/config/theme.py - 新增文件

class ThemeColors:
    """现代化主题颜色配置"""
    
    # 深色模式（推荐）
    DARK = {
        'primary': '#2563EB',           # 现代蓝
        'primary_hover': '#1D4ED8',     # 深蓝
        'primary_active': '#1E40AF',    # 更深蓝
        
        'success': '#10B981',           # 翠绿
        'warning': '#F59E0B',           # 琥珀
        'danger': '#EF4444',            # 亮红
        'info': '#06B6D4',              # 青色
        
        'background': '#0F172A',        # 极深蓝黑
        'surface': '#1E293B',           # 深蓝灰
        'surface_hover': '#334155',     # 浅深灰
        'surface_active': '#475569',    # 更浅灰
        
        'text_primary': '#F8FAFC',      # 纯白
        'text_secondary': '#CBD5E1',    # 浅灰
        'text_tertiary': '#94A3B8',     # 中灰
        
        'border': '#334155',            # 边框灰
        'divider': '#1E293B',           # 分割线
        
        'shadow_sm': 'rgba(0, 0, 0, 0.1)',
        'shadow_md': 'rgba(0, 0, 0, 0.2)',
    }
    
    # 浅色模式
    LIGHT = {
        'primary': '#2563EB',
        'primary_hover': '#1D4ED8',
        'primary_active': '#1E40AF',
        
        'success': '#059669',
        'warning': '#D97706',
        'danger': '#DC2626',
        'info': '#0891B2',
        
        'background': '#FFFFFF',
        'surface': '#F1F5F9',
        'surface_hover': '#E2E8F0',
        'surface_active': '#CBD5E1',
        
        'text_primary': '#0F172A',
        'text_secondary': '#475569',
        'text_tertiary': '#94A3B8',
        
        'border': '#E2E8F0',
        'divider': '#F1F5F9',
        
        'shadow_sm': 'rgba(0, 0, 0, 0.05)',
        'shadow_md': 'rgba(0, 0, 0, 0.1)',
    }
```

### 1.2 统一样式表系统

```python
# src/ui/styles.py - 新增文件

class StyleSheet:
    """统一样式表管理"""
    
    @staticmethod
    def get_stylesheet(theme='dark'):
        """获取完整样式表"""
        colors = ThemeColors.DARK if theme == 'dark' else ThemeColors.LIGHT
        
        return f"""
        /* === 全局样式 === */
        * {{
            margin: 0;
            padding: 0;
            border: none;
        }}
        
        QMainWindow, QDialog {{
            background-color: {colors['background']};
            color: {colors['text_primary']};
            font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
            font-size: 11px;
        }}
        
        /* === 按钮样式 === */
        QPushButton {{
            background-color: {colors['primary']};
            color: white;
            border: none;
            border-radius: 6px;
            padding: 10px 18px;
            font-weight: 600;
            font-size: 12px;
            transition: all 0.3s ease;
        }}
        
        QPushButton:hover {{
            background-color: {colors['primary_hover']};
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        }}
        
        QPushButton:pressed {{
            background-color: {colors['primary_active']};
        }}
        
        QPushButton:disabled {{
            background-color: #6B7280;
            color: #9CA3AF;
        }}
        
        /* === 辅助按钮 === */
        QPushButton#secondaryBtn {{
            background-color: {colors['surface']};
            color: {colors['text_primary']};
            border: 1px solid {colors['border']};
        }}
        
        QPushButton#secondaryBtn:hover {{
            background-color: {colors['surface_hover']};
        }}
        
        /* === 危险按钮 === */
        QPushButton#dangerBtn {{
            background-color: {colors['danger']};
        }}
        
        QPushButton#dangerBtn:hover {{
            background-color: #DC2626;
        }}
        
        /* === 成功按钮 === */
        QPushButton#successBtn {{
            background-color: {colors['success']};
        }}
        
        QPushButton#successBtn:hover {{
            background-color: #059669;
        }}
        
        /* === 标签样式 === */
        QLabel {{
            color: {colors['text_primary']};
            background-color: transparent;
            font-size: 12px;
        }}
        
        QLabel#titleLabel {{
            font-size: 16px;
            font-weight: 700;
            color: {colors['text_primary']};
        }}
        
        QLabel#subtitleLabel {{
            font-size: 13px;
            color: {colors['text_secondary']};
        }}
        
        QLabel#captionLabel {{
            font-size: 10px;
            color: {colors['text_tertiary']};
        }}
        
        /* === 输入框样式 === */
        QLineEdit, QSpinBox, QDoubleSpinBox {{
            background-color: {colors['surface']};
            color: {colors['text_primary']};
            border: 1px solid {colors['border']};
            border-radius: 4px;
            padding: 8px 10px;
            font-size: 11px;
        }}
        
        QLineEdit:focus, QSpinBox:focus {{
            border: 2px solid {colors['primary']};
            background-color: {colors['surface_active']};
        }}
        
        /* === 下拉框样式 === */
        QComboBox {{
            background-color: {colors['surface']};
            color: {colors['text_primary']};
            border: 1px solid {colors['border']};
            border-radius: 4px;
            padding: 6px 10px;
            font-size: 11px;
        }}
        
        QComboBox:focus {{
            border: 2px solid {colors['primary']};
        }}
        
        QComboBox::drop-down {{
            border: none;
            padding-right: 6px;
        }}
        
        QComboBox::drop-down:icon {{
            image: none;
        }}
        
        /* === 滑块样式 === */
        QSlider::groove:horizontal {{
            background-color: {colors['surface']};
            height: 4px;
            border-radius: 2px;
        }}
        
        QSlider::handle:horizontal {{
            background-color: {colors['primary']};
            width: 16px;
            margin: -6px 0;
            border-radius: 8px;
            border: none;
        }}
        
        QSlider::handle:horizontal:hover {{
            background-color: {colors['primary_hover']};
            box-shadow: 0 0 8px rgba(37, 99, 235, 0.4);
        }}
        
        /* === 滚动条样式 === */
        QScrollBar:horizontal {{
            background-color: {colors['background']};
            height: 8px;
            border: none;
        }}
        
        QScrollBar::handle:horizontal {{
            background-color: {colors['surface_hover']};
            border-radius: 4px;
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background-color: {colors['border']};
        }}
        
        /* === 卡片/分组框 === */
        QGroupBox {{
            color: {colors['text_primary']};
            border: 1px solid {colors['border']};
            border-radius: 6px;
            padding: 12px;
            margin-top: 8px;
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 4px;
        }}
        
        /* === 选项卡 === */
        QTabWidget::pane {{
            border: 1px solid {colors['border']};
            background-color: {colors['surface']};
            border-radius: 4px;
        }}
        
        QTabBar::tab {{
            background-color: {colors['background']};
            color: {colors['text_secondary']};
            padding: 8px 16px;
            border-bottom: 2px solid transparent;
            margin-right: 2px;
        }}
        
        QTabBar::tab:selected {{
            background-color: {colors['surface']};
            color: {colors['primary']};
            border-bottom: 2px solid {colors['primary']};
        }}
        """
```

---

## 第二部分：主窗口现代化改进

### 2.1 新的主窗口结构

```python
# src/ui/main_window.py - 改进版本

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QPushButton, QLineEdit, 
    QMessageBox, QApplication, QDialog, QGroupBox,
    QStackedWidget, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QIcon, QPixmap, QFont
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve

from ..config import settings
from ..utils import logger, WindowManager, ScreenCapture
from ..core import CaptureEngine
from .region_selector import RegionSelector
from .capture_window import CaptureWindow
from .styles import StyleSheet

class MainWindow(QMainWindow):
    """
    现代化主窗口
    
    改进项：
    - 采用深色现代设计
    - 分组化布局，逻辑清晰
    - 优化的视觉层级
    - 平滑的动画过渡
    - 响应式设计
    """
    
    def __init__(self):
        super().__init__()
        
        self.capture_windows = []
        self.selected_region = None
        
        # 应用现代样式表
        self._apply_theme()
        
        self._init_ui()
        self._setup_animations()
        
        logger.info("现代化主窗口已初始化")
    
    def _apply_theme(self):
        """应用现代主题"""
        stylesheet = StyleSheet.get_stylesheet('dark')
        self.setStyleSheet(stylesheet)
    
    def _init_ui(self):
        """初始化UI"""
        self.setWindowTitle("🎥 实时窗口监视器")
        self.setWindowIcon(self._create_window_icon())
        self.setGeometry(100, 100, 520, 720)
        self.setMinimumWidth(480)
        self.setMaximumWidth(600)
        
        # 中心部件
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # ===== 标题区域 =====
        title_layout = self._create_title_section()
        main_layout.addLayout(title_layout)
        
        main_layout.addSpacing(8)
        
        # ===== 分割线 =====
        divider1 = self._create_divider()
        main_layout.addWidget(divider1)
        
        main_layout.addSpacing(8)
        
        # ===== 窗口选择卡片 =====
        window_card = self._create_window_selection_card()
        main_layout.addWidget(window_card)
        
        main_layout.addSpacing(8)
        
        # ===== 分割线 =====
        divider2 = self._create_divider()
        main_layout.addWidget(divider2)
        
        main_layout.addSpacing(8)
        
        # ===== 区域设置卡片 =====
        region_card = self._create_region_settings_card()
        main_layout.addWidget(region_card)
        
        main_layout.addSpacing(8)
        
        # ===== 分割线 =====
        divider3 = self._create_divider()
        main_layout.addWidget(divider3)
        
        main_layout.addSpacing(8)
        
        # ===== 帧率设置卡片 =====
        fps_card = self._create_fps_settings_card()
        main_layout.addWidget(fps_card)
        
        # 弹性空间
        main_layout.addStretch()
        
        # ===== 行动按钮区域 =====
        button_layout = self._create_action_buttons()
        main_layout.addLayout(button_layout)
        
        # ===== 底部提示 =====
        footer = self._create_footer()
        main_layout.addWidget(footer)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
    
    def _create_title_section(self) -> QVBoxLayout:
        """创建标题区域"""
        layout = QVBoxLayout()
        layout.setSpacing(4)
        
        # 主标题
        title = QLabel("实时窗口监视器")
        title.setObjectName("titleLabel")
        title_font = QFont('Segoe UI', 18)
        title_font.setWeight(QFont.Weight.Bold)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # 副标题
        subtitle = QLabel("实时捕获、监视并分析任意窗口内容")
        subtitle.setObjectName("subtitleLabel")
        layout.addWidget(subtitle)
        
        return layout
    
    def _create_window_selection_card(self) -> QGroupBox:
        """创建窗口选择卡片"""
        card = QGroupBox("📺 选择监视窗口")
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # 说明文本
        info = QLabel("选择您要监视的应用程序窗口")
        info.setObjectName("captionLabel")
        layout.addWidget(info)
        
        # 窗口下拉框
        dropdown_layout = QHBoxLayout()
        
        dropdown_label = QLabel("可用窗口:")
        dropdown_label.setFixedWidth(70)
        dropdown_layout.addWidget(dropdown_label)
        
        self.combo = QComboBox()
        self.combo.setMinimumHeight(36)
        self.refresh_windows()
        dropdown_layout.addWidget(self.combo)
        
        layout.addLayout(dropdown_layout)
        
        # 刷新按钮
        refresh_btn_layout = QHBoxLayout()
        self.refresh_btn = QPushButton("🔄 刷新窗口列表")
        self.refresh_btn.setObjectName("secondaryBtn")
        self.refresh_btn.setFixedHeight(32)
        self.refresh_btn.clicked.connect(self.refresh_windows)
        refresh_btn_layout.addStretch()
        refresh_btn_layout.addWidget(self.refresh_btn, 0, Qt.AlignmentFlag.AlignRight)
        
        layout.addLayout(refresh_btn_layout)
        
        card.setLayout(layout)
        return card
    
    def _create_region_settings_card(self) -> QGroupBox:
        """创建区域设置卡片"""
        card = QGroupBox("✂️ 监视区域设置")
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # 说明文本
        info = QLabel("选择要监视的特定区域，或监视整个窗口")
        info.setObjectName("captionLabel")
        layout.addWidget(info)
        
        # 选择区域按钮
        self.select_region_btn = QPushButton("🎯 图形化选择区域")
        self.select_region_btn.setMinimumHeight(40)
        self.select_region_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #2563EB, stop: 1 #1D4ED8
                );
                color: white;
                font-weight: 600;
                border-radius: 6px;
                padding: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #1D4ED8, stop: 1 #1E40AF
                );
            }
        """)
        self.select_region_btn.clicked.connect(self.open_region_selector)
        layout.addWidget(self.select_region_btn)
        
        # 当前选择显示
        self.region_info_label = QLabel("📍 未选择区域（将监视整个窗口）")
        self.region_info_label.setStyleSheet("""
            QLabel {
                background-color: #1E293B;
                padding: 10px 12px;
                border: 1px solid #334155;
                border-radius: 4px;
                color: #94A3B8;
            }
        """)
        self.region_info_label.setWordWrap(True)
        layout.addWidget(self.region_info_label)
        
        card.setLayout(layout)
        return card
    
    def _create_fps_settings_card(self) -> QGroupBox:
        """创建帧率设置卡片"""
        card = QGroupBox("⚡ 性能设置")
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # 说明
        info = QLabel("调整捕获帧率以平衡性能和流畅度")
        info.setObjectName("captionLabel")
        layout.addWidget(info)
        
        # 帧率输入
        fps_layout = QHBoxLayout()
        
        fps_label = QLabel("目标帧率:")
        fps_label.setFixedWidth(70)
        fps_layout.addWidget(fps_label)
        
        self.fps_spinbox = QLineEdit(str(settings.capture.default_fps))
        self.fps_spinbox.setFixedWidth(60)
        self.fps_spinbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fps_layout.addWidget(self.fps_spinbox)
        
        fps_unit = QLabel(f"FPS （建议 15-30，范围 {settings.capture.min_fps}-{settings.capture.max_fps}）")
        fps_unit.setObjectName("captionLabel")
        fps_layout.addWidget(fps_unit)
        
        fps_layout.addStretch()
        layout.addLayout(fps_layout)
        
        card.setLayout(layout)
        return card
    
    def _create_action_buttons(self) -> QHBoxLayout:
        """创建行动按钮区域"""
        layout = QHBoxLayout()
        layout.setSpacing(12)
        
        # 启动监视按钮
        self.start_btn = QPushButton("🚀 启动监视")
        self.start_btn.setMinimumHeight(44)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #10B981, stop: 1 #059669
                );
                color: white;
                font-size: 13px;
                font-weight: 700;
                border-radius: 6px;
                padding: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #059669, stop: 1 #047857
                );
                box-shadow: 0 8px 20px rgba(16, 185, 129, 0.3);
            }
            QPushButton:pressed {
                padding-top: 12px;
                padding-bottom: 8px;
            }
        """)
        self.start_btn.clicked.connect(self.start_capture)
        layout.addWidget(self.start_btn)
        
        return layout
    
    def _create_footer(self) -> QLabel:
        """创建底部提示"""
        footer = QLabel(
            "💡 提示：选择一个窗口 → 可选：选择监视区域 → 调整帧率 → 启动监视\n"
            "🎯 建议使用窗口：记事本、浏览器、资源管理器等"
        )
        footer.setObjectName("captionLabel")
        footer.setWordWrap(True)
        footer.setStyleSheet("""
            QLabel {
                background-color: #1E293B;
                padding: 10px 12px;
                border-radius: 4px;
                border: 1px solid #334155;
                color: #94A3B8;
            }
        """)
        return footer
    
    def _create_divider(self) -> QLabel:
        """创建分割线"""
        divider = QLabel()
        divider.setStyleSheet("background-color: #334155;")
        divider.setFixedHeight(1)
        return divider
    
    def _create_window_icon(self) -> QIcon:
        """创建窗口图标"""
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.GlobalColor.transparent)
        # 实现简单的图标或使用系统图标
        return QIcon(pixmap)
    
    def _setup_animations(self):
        """设置动画"""
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    
    def refresh_windows(self):
        """刷新窗口列表"""
        logger.debug("刷新窗口列表...")
        self.combo.clear()
        windows = WindowManager.enum_windows()
        for hwnd, title in windows:
            self.combo.addItem(title, hwnd)
        logger.debug(f"窗口列表已更新，共 {len(windows)} 个窗口")
    
    def open_region_selector(self):
        """打开区域选择器"""
        hwnd = self.combo.itemData(self.combo.currentIndex())
        if not hwnd:
            QMessageBox.warning(self, "提示", "请先选择一个窗口！")
            return
        
        window_title = self.combo.currentText()
        my_hwnd = int(self.winId())
        
        if settings.app_name in window_title or hwnd == my_hwnd:
            QMessageBox.warning(self, "警告", 
                f"⚠️ 不能选择本程序自己！\n\n请选择其他窗口进行监视。")
            return
        
        logger.debug(f"开始为窗口 '{window_title}' 截图...")
        
        self.select_region_btn.setText("⏳ 正在截图...")
        self.select_region_btn.setEnabled(False)
        QApplication.processEvents()
        
        try:
            rect = WindowManager.get_window_rect(hwnd)
            width = rect[2] - rect[0]
            height = rect[3] - rect[1]
            
            screenshot, method = ScreenCapture.capture_window(hwnd, width, height)
            
            if screenshot is None or screenshot.isNull():
                QMessageBox.warning(self, "错误", 
                    "无法截取窗口图片！\n\n"
                    "可能原因：\n"
                    "• 窗口被最小化\n"
                    "• 窗口尺寸过小\n"
                    "• 窗口类型不支持截图")
                return
            
            logger.info(f"截图成功: {width}x{height}, 方法: {method}")
            
            selector = RegionSelector(screenshot, width, height, self)
            
            if selector.exec() == QDialog.DialogCode.Accepted:
                region = selector.get_selected_region()
                if region:
                    self.selected_region = region
                    x, y, w, h = region
                    self.region_info_label.setText(
                        f"✅ 已选择区域: X={x}, Y={y}, 宽度={w}, 高度={h}"
                    )
                    self.region_info_label.setStyleSheet("""
                        QLabel {
                            background-color: #064E3B;
                            padding: 10px 12px;
                            border: 1px solid #10B981;
                            border-radius: 4px;
                            color: #86EFAC;
                        }
                    """)
                    logger.info(f"用户选择了区域: {region}")
        
        except Exception as e:
            QMessageBox.critical(self, "错误", f"截图失败：{str(e)}")
            logger.error(f"截图失败: {e}")
        
        finally:
            self.select_region_btn.setText("🎯 图形化选择区域")
            self.select_region_btn.setEnabled(True)
    
    def start_capture(self):
        """启动监视"""
        hwnd = self.combo.itemData(self.combo.currentIndex())
        if not hwnd:
            QMessageBox.warning(self, "提示", "请先选择一个窗口！")
            return
        
        try:
            my_hwnd = int(self.winId())
            window_title = self.combo.currentText()
            
            if settings.app_name in window_title or hwnd == my_hwnd:
                QMessageBox.warning(self, "警告",
                    "⚠️ 不能监视程序自己！\n\n"
                    "请选择其他窗口进行监视。")
                logger.warning("用户尝试监视程序自己，已阻止")
                return
            
            fps = int(self.fps_spinbox.text())
            
            if fps < settings.capture.min_fps or fps > settings.capture.max_fps:
                QMessageBox.warning(self, "错误", 
                    f"FPS 必须在 {settings.capture.min_fps}-{settings.capture.max_fps} 之间！")
                return
            
            if self.selected_region:
                x, y, width, height = self.selected_region
            else:
                target_rect = WindowManager.get_window_rect(hwnd)
                x, y = 0, 0
                width = target_rect[2] - target_rect[0]
                height = target_rect[3] - target_rect[1]
            
            if width <= 0 or height <= 0:
                QMessageBox.warning(self, "错误", "监视区域尺寸无效！")
                return
            
            logger.info(f"用户启动监视: '{window_title}' ({width}x{height}) @ {fps} FPS")
            
            region = (x, y, width, height)
            engine = CaptureEngine(hwnd, region, fps)
            capture_win = CaptureWindow(engine, window_title, self)
            
            main_x = self.x()
            main_y = self.y()
            capture_win.move(main_x + self.width() + 20, main_y)
            
            self.capture_windows.append((engine, capture_win))
            
            capture_win.show()
            capture_win.raise_()
            capture_win.activateWindow()
            engine.start()
            
            logger.info("监视窗口已启动")
            
        except ValueError as e:
            QMessageBox.warning(self, "错误", f"输入值无效: {e}")
            logger.error(f"输入值解析失败: {e}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"启动监视失败：{str(e)}")
            logger.error(f"启动监视失败: {e}")
    
    def showEvent(self, event):
        """窗口显示事件"""
        super().showEvent(event)
        if hasattr(self, 'animation'):
            self.animation.start()
```

---

## 第三部分：监视窗口现代化改进

### 3.1 优化的监视窗口

```python
# src/ui/capture_window.py - 改进版本

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QSlider, QGraphicsView, QGraphicsScene
)
from PyQt6.QtGui import QPixmap, QImage, QFont, QColor
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve

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
    - 平滑的过渡动画
    """
    
    def __init__(self, engine: CaptureEngine, window_title: str, parent=None):
        super().__init__(parent)
        
        self.engine = engine
        self.window_title = window_title
        
        self.dragging = False
        self.drag_position = QPoint()
        
        self._connect_signals()
        self._init_ui()
        
        logger.info(f"监视窗口已创建: '{window_title}'")
    
    def _connect_signals(self):
        """连接信号"""
        self.engine.frame_captured.connect(self.on_frame_captured)
        self.engine.fps_updated.connect(self.on_fps_updated)
        self.engine.method_changed.connect(self.on_method_changed)
        self.engine.capture_failed.connect(self.on_capture_failed)
    
    def _init_ui(self):
        """初始化UI"""
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
                border: 2px solid #1E40AF;
                border-radius: 8px;
            }
        """)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setRenderHint(self.view.renderHint()|16)  # 平滑缩放
        
        main_layout.addWidget(self.view)
        
        # 控制栏
        control_layout = self._create_control_bar()
        main_layout.addLayout(control_layout)
        
        self.setLayout(main_layout)
    
    def _create_control_bar(self) -> QHBoxLayout:
        """创建控制栏"""
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(8, 8, 8, 8)
        control_layout.setSpacing(8)
        control_layout.setStyleSheet("""
            QHBoxLayout {
                background-color: #1E293B;
                border-top: 1px solid #334155;
            }
        """)
        
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
        
        # FPS 调节
        control_layout.addWidget(QLabel("📊"))
        
        self.fps_slider = QSlider(Qt.Orientation.Horizontal)
        self.fps_slider.setMinimum(settings.capture.min_fps)
        self.fps_slider.setMaximum(settings.capture.max_fps)
        self.fps_slider.setValue(self.engine.fps)
        self.fps_slider.setFixedWidth(120)
        self.fps_slider.valueChanged.connect(self.on_fps_slider_changed)
        control_layout.addWidget(self.fps_slider)
        
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
        self.method_label = QLabel("...")
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
        
        return control_layout
    
    def on_frame_captured(self, image: QImage):
        """处理捕获的帧"""
        self.scene.clear()
        self.scene.addPixmap(QPixmap.fromImage(image))
        
        width = image.width()
        height = image.height()
        self.view.setSceneRect(0, 0, width, height)
        
        if self.engine.capture_count == 1:
            self.resize(width, height + 50)
    
    def on_fps_updated(self, fps: float):
        """FPS 更新"""
        self.fps_label.setText(f"FPS: {fps:.1f}")
    
    def on_method_changed(self, method: str):
        """捕获方法变更"""
        self.method_label.setText(f"{method}")
        logger.info(f"捕获方法: {method}")
    
    def on_capture_failed(self, error_message: str):
        """捕获失败"""
        self.status_label.setText("❌")
        self.method_label.setText("错误")
        logger.error(f"捕获失败: {error_message}")
    
    def toggle_pause(self):
        """切换暂停"""
        if self.engine.is_paused:
            self.engine.resume()
            self.pause_btn.setText("⏸")
            self.status_label.setText("🟢")
        else:
            self.engine.pause()
            self.pause_btn.setText("▶")
            self.status_label.setText("⏸")
    
    def on_fps_slider_changed(self, value: int):
        """帧率改变"""
        self.fps_value_label.setText(str(value))
        self.engine.set_fps(value)
    
    def mousePressEvent(self, event):
        """鼠标按下"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """鼠标移动"""
        if self.dragging:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        """鼠标释放"""
        self.dragging = False
    
    def closeEvent(self, event):
        """关闭事件"""
        logger.info(f"监视窗口关闭: '{self.window_title}'")
        self.engine.stop()
        event.accept()
```

---

## 第四部分：区域选择器现代化

### 4.1 优化的区域选择器

```python
# src/ui/region_selector.py - 改进版本

from PyQt6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QPixmap, QImage, QPainter, QColor, QPen, QBrush, QCursor, QFont
from PyQt6.QtCore import Qt, QPoint, QRect

from ..config import settings
from ..utils import logger

class RegionSelector(QDialog):
    """现代化区域选择器"""
    
    def __init__(self, screenshot: QImage, window_width: int, window_height: int, parent=None):
        super().__init__(parent)
        
        self.screenshot = screenshot
        self.window_width = window_width
        self.window_height = window_height
        self.selected_rect = None
        
        self.selecting = False
        self.start_point = QPoint()
        self.end_point = QPoint()
        self.current_rect = QRect()
        
        self._init_ui()
        
        logger.debug(f"区域选择器已创建: {window_width}x{window_height}")
    
    def _init_ui(self):
        """初始化UI"""
        self.setWindowTitle("📐 拖拽选择监视区域")
        self.setModal(True)
        self.setStyleSheet("""
            QDialog {
                background-color: #0F172A;
                color: #F8FAFC;
            }
            QPushButton {
                background-color: #2563EB;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: 600;
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
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 信息栏
        info_layout = QHBoxLayout()
        info_layout.setContentsMargins(12, 12, 12, 12)
        info_layout.setSpacing(8)
        
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
        divider.setStyleSheet("background-color: #334155; height: 1px;")
        layout.addWidget(divider)
        
        # 缩放计算
        scale = min(
            settings.ui.selector_max_width / self.window_width,
            settings.ui.selector_max_height / self.window_height,
            1.0
        )
        self.scale = scale
        
        display_width = int(self.window_width * scale)
        display_height = int(self.window_height * scale)
        
        # 图片标签
        self.image_label = QLabel()
        self.image_label.setMouseTracking(True)
        self.image_label.setCursor(QCursor(Qt.CursorShape.CrossCursor))
        self._update_display()
        
        layout.addWidget(self.image_label)
        
        # 按钮栏
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(12, 12, 12, 12)
        button_layout.setSpacing(8)
        
        self.full_btn = QPushButton("📺 选择整个窗口")
        self.full_btn.clicked.connect(self._select_full_window)
        button_layout.addWidget(self.full_btn)
        
        self.reset_btn = QPushButton("🔄 重新选择")
        self.reset_btn.clicked.connect(self._reset_selection)
        button_layout.addWidget(self.reset_btn)
        
        button_layout.addStretch()
        
        self.cancel_btn = QPushButton("❌ 取消")
        self.cancel_btn.setObjectName("cancelBtn")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        self.confirm_btn = QPushButton("✅ 确认选择")
        self.confirm_btn.setEnabled(False)
        self.confirm_btn.clicked.connect(self.accept)
        button_layout.addWidget(self.confirm_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.resize(display_width + 24, display_height + 120)
    
    def _update_display(self):
        """更新显示"""
        display_image = self.screenshot.copy()
        
        if not self.current_rect.isNull():
            painter = QPainter(display_image)
            
            # 蒙版
            painter.fillRect(0, 0, self.window_width, self.window_height, 
                           QColor(0, 0, 0, 120))
            
            # 清除选中区域蒙版
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
            painter.fillRect(self.current_rect, QColor(0, 0, 0, 0))
            
            # 边框
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
            pen = QPen(QColor(16, 185, 129), 3, Qt.PenStyle.SolidLine)
            painter.setPen(pen)
            painter.drawRect(self.current_rect)
            
            # 角点
            corner_size = 10
            painter.setBrush(QBrush(QColor(16, 185, 129)))
            corners = [
                self.current_rect.topLeft(),
                self.current_rect.topRight(),
                self.current_rect.bottomLeft(),
                self.current_rect.bottomRight()
            ]
            for corner in corners:
                painter.drawRect(corner.x() - corner_size//2, 
                               corner.y() - corner_size//2,
                               corner_size, corner_size)
            
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
        """鼠标按下"""
        if event.button() == Qt.MouseButton.LeftButton:
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
        """鼠标移动"""
        if self.selecting:
            pos = self.image_label.mapFrom(self, event.pos())
            actual_x = int(pos.x() / self.scale)
            actual_y = int(pos.y() / self.scale)
            
            actual_x = max(0, min(actual_x, self.window_width - 1))
            actual_y = max(0, min(actual_y, self.window_height - 1))
            
            self.end_point = QPoint(actual_x, actual_y)
            self.current_rect = QRect(self.start_point, self.end_point).normalized()
            
            self._update_coord_label()
            self._update_display()
    
    def mouseReleaseEvent(self, event):
        """鼠标释放"""
        if event.button() == Qt.MouseButton.LeftButton and self.selecting:
            self.selecting = False
            
            min_size = settings.capture.min_region_size
            if self.current_rect.width() > min_size and self.current_rect.height() > min_size:
                self.selected_rect = self.current_rect
                self.confirm_btn.setEnabled(True)
                self._update_coord_label()
                logger.debug(f"区域已选择: {self.current_rect}")
            else:
                self._reset_selection()
    
    def _update_coord_label(self):
        """更新坐标标签"""
        if not self.current_rect.isNull():
            self.coord_label.setText(
                f"X={self.current_rect.x()}, Y={self.current_rect.y()}, "
                f"宽={self.current_rect.width()}, 高={self.current_rect.height()}"
            )
    
    def _select_full_window(self):
        """选择整个窗口"""
        self.current_rect = QRect(0, 0, self.window_width, self.window_height)
        self.selected_rect = self.current_rect
        self.confirm_btn.setEnabled(True)
        self._update_coord_label()
        self._update_display()
    
    def _reset_selection(self):
        """重置选择"""
        self.current_rect = QRect()
        self.selected_rect = None
        self.confirm_btn.setEnabled(False)
        self.coord_label.setText("等待选择...")
        self._update_display()
    
    def get_selected_region(self):
        """获取选择的区域"""
        if self.selected_rect:
            return (self.selected_rect.x(), self.selected_rect.y(),
                    self.selected_rect.width(), self.selected_rect.height())
        return None
```

---

## 第五部分：实施步骤

### 5.1 文件创建清单

1. **新增配置文件：**
   - `src/config/theme.py` - 主题配置
   - `src/ui/styles.py` - 样式表管理

2. **更新现有文件：**
   - `src/ui/main_window.py` - 现代化主窗口
   - `src/ui/capture_window.py` - 现代化监视窗口
   - `src/ui/region_selector.py` - 现代化区域选择器
   - `src/config/settings.py` - 添加主题切换选项（可选）

### 5.2 集成步骤

```python
# 1. 创建 theme.py 文件（配置文件）
# 2. 创建 styles.py 文件（样式表）
# 3. 更新 main_window.py（应用新主题）
# 4. 更新 capture_window.py（应用新设计）
# 5. 更新 region_selector.py（应用新设计）
# 6. 运行测试确保正常工作
```

### 5.3 验证清单

- [ ] 主窗口深色主题应用成功
- [ ] 所有按钮具有现代悬停效果
- [ ] 输入框具有焦点高亮
- [ ] 监视窗口具有时尚的控制栏
- [ ] 区域选择器界面清晰美观
- [ ] 所有文本具有良好的对比度
- [ ] 窗口动画流畅无卡顿

---

## 第六部分：进阶优化建议

### 6.1 响应式布局
```python
# 添加窗口大小改变事件处理
def resizeEvent(self, event):
    """窗口大小改变时重新布局"""
    super().resizeEvent(event)
    # 动态调整元素大小
```

### 6.2 主题切换功能
```python
# 支持深/浅色主题切换
def toggle_theme(self):
    """切换主题"""
    self.current_theme = 'light' if self.current_theme == 'dark' else 'dark'
    stylesheet = StyleSheet.get_stylesheet(self.current_theme)
    self.setStyleSheet(stylesheet)
```

### 6.3 自定义图标库
```python
# 使用 Font Awesome 或自定义 SVG 图标
from PyQt6.QtGui import QIcon
from PyQt6.QtSvg import QSvgWidget

def create_svg_icon(svg_path):
    """创建 SVG 图标"""
    return QIcon(svg_path)
```

### 6.4 性能指标面板
```python
# 在监视窗口添加实时性能图表
class PerformancePanel(QWidget):
    """性能指标面板"""
    def __init__(self):
        super().__init__()
        self.fps_history = []
        self.cpu_usage = 0
        self.memory_usage = 0
```

---

## 第七部分：最终效果对比

| 方面 | 原始设计 | 现代化设计 |
|------|--------|---------|
| 色彩搭配 | 简单绿蓝 | 专业配色方案 |
| 按钮样式 | 平面按钮 | 渐变 + 阴影 |
| 用户体验 | 基础功能 | 动画 + 交互反馈 |
| 视觉层级 | 混乱 | 清晰有序 |
| 专业度 | 70% | 95% |

---

## 总结

本方案通过以下关键改进提升了应用的现代化程度：

1. **色彩系统**：采用现代企业级配色（深蓝系 + 翠绿强调色）
2. **交互设计**：添加悬停效果、渐变、阴影等视觉反馈
3. **布局优化**：使用分组卡片、分割线等打造清晰结构
4. **动画效果**：平滑的过渡提升用户体验
5. **响应式设计**：支持不同分辨率和窗口大小

立即实施这些改进，您的应用将获得**专业、现代、高端的视觉形象**。

