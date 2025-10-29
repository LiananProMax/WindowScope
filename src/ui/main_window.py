"""
主窗口 UI 组件 - 现代化版本
提供窗口选择和配置界面
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QComboBox, QPushButton, QLineEdit, 
                             QMessageBox, QApplication, QDialog, QGroupBox)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QIcon, QPixmap

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
        """初始化主窗口"""
        super().__init__()
        
        # 保存监视窗口引用（防止垃圾回收）
        self.capture_windows = []
        
        # 选择的区域（None 表示整个窗口）
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
        """初始化用户界面"""
        self.setWindowTitle("🪟 WindowScope")
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
        main_layout.addWidget(self._create_divider())
        main_layout.addSpacing(8)
        
        # ===== 窗口选择卡片 =====
        window_card = self._create_window_selection_card()
        main_layout.addWidget(window_card)
        
        main_layout.addSpacing(8)
        
        # ===== 分割线 =====
        main_layout.addWidget(self._create_divider())
        main_layout.addSpacing(8)
        
        # ===== 区域设置卡片 =====
        region_card = self._create_region_settings_card()
        main_layout.addWidget(region_card)
        
        main_layout.addSpacing(8)
        
        # ===== 分割线 =====
        main_layout.addWidget(self._create_divider())
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
        title = QLabel("WindowScope")
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
        self.select_region_btn.setStyleSheet(StyleSheet.get_button_secondary())
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
        self.start_btn.setStyleSheet(StyleSheet.get_button_primary())
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
                padding: 12px;
                border-radius: 6px;
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
        
        logger.debug(f"窗口列表已更新，下拉框中有 {len(windows)} 个选项")
    
    def open_region_selector(self):
        """打开图形化区域选择器"""
        hwnd = self.combo.itemData(self.combo.currentIndex())
        if not hwnd:
            QMessageBox.warning(self, "提示", "请先选择一个窗口！")
            return
        
        # 检查是否选择了自己
        window_title = self.combo.currentText()
        my_hwnd = int(self.winId())
        
        if settings.app_name in window_title or hwnd == my_hwnd:
            QMessageBox.warning(self, "警告", 
                f"⚠️ 不能选择本程序自己！\n\n请选择其他窗口进行监视。")
            return
        
        logger.debug(f"开始为窗口 '{window_title}' 截图...")
        
        # 显示等待提示
        self.select_region_btn.setText("⏳ 正在截图...")
        self.select_region_btn.setEnabled(False)
        QApplication.processEvents()
        
        try:
            # 获取窗口尺寸并截图
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
                    "• 窗口类型不支持截图\n\n"
                    "请确保窗口正常显示后重试。")
                return
            
            logger.info(f"截图成功: {width}x{height}, 方法: {method}")
            
            # 打开区域选择器
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
            else:
                logger.debug("用户取消了区域选择")
                
        except Exception as e:
            QMessageBox.critical(self, "错误", f"截图失败：{str(e)}")
            logger.error(f"截图失败: {e}")
        finally:
            # 恢复按钮状态
            self.select_region_btn.setText("🎯 图形化选择区域")
            self.select_region_btn.setEnabled(True)
    
    def start_capture(self):
        """开始监视选定的窗口"""
        hwnd = self.combo.itemData(self.combo.currentIndex())
        if not hwnd:
            QMessageBox.warning(self, "提示", "请先选择一个窗口！")
            return
        
        try:
            # 检查是否选择了自己
            my_hwnd = int(self.winId())
            window_title = self.combo.currentText()
            
            if settings.app_name in window_title or hwnd == my_hwnd:
                QMessageBox.warning(self, "警告",
                    "⚠️ 不能监视程序自己！\n\n"
                    "请选择其他窗口进行监视。\n"
                    "建议：打开记事本、浏览器等其他应用来测试。")
                logger.warning("用户尝试监视程序自己，已阻止")
                return
            
            # 获取帧率
            fps = int(self.fps_spinbox.text())
            
            # 验证 FPS 范围
            if fps < settings.capture.min_fps or fps > settings.capture.max_fps:
                QMessageBox.warning(self, "错误", 
                    f"FPS 必须在 {settings.capture.min_fps}-{settings.capture.max_fps} 之间！")
                return
            
            # 确定监视区域
            if self.selected_region:
                # 使用图形化选择的区域
                x, y, width, height = self.selected_region
            else:
                # 使用整个窗口
                target_rect = WindowManager.get_window_rect(hwnd)
                x, y = 0, 0
                width = target_rect[2] - target_rect[0]
                height = target_rect[3] - target_rect[1]
            
            # 验证尺寸
            if width <= 0 or height <= 0:
                QMessageBox.warning(self, "错误", "监视区域尺寸无效！")
                return
            
            logger.info(f"{'*'*60}")
            logger.info(f"用户启动实时监视:")
            logger.info(f"  选中窗口: '{window_title}'")
            logger.info(f"  HWND: {hwnd}")
            logger.info(f"  裁剪参数: x={x}, y={y}, width={width}, height={height}")
            logger.info(f"  目标帧率: {fps} FPS")
            logger.info(f"{'*'*60}")
            
            region = (x, y, width, height)
            
            # 创建捕获引擎
            engine = CaptureEngine(hwnd, region, fps)
            
            # 创建监视窗口
            capture_win = CaptureWindow(engine, window_title, self)
            
            # 设置窗口初始位置（在主窗口右侧）
            main_x = self.x()
            main_y = self.y()
            capture_win.move(main_x + self.width() + 20, main_y)
            logger.debug(f"监视窗口位置: x={main_x + self.width() + 20}, y={main_y}")
            
            # 保存引用，防止被垃圾回收
            self.capture_windows.append((engine, capture_win))
            
            # 显示窗口并启动引擎
            capture_win.show()
            capture_win.raise_()
            capture_win.activateWindow()
            engine.start()
            
            logger.info("监视窗口已显示并激活，实时视频流开始")
            print(f"\n✅ 监视窗口已启动！")
            print(f"   窗口标题: 监视: {window_title}")
            print(f"   位置: 主窗口右侧")
            print(f"   帧率: {fps} FPS")
            print(f"   已启动监视窗口数: {len(self.capture_windows)}\n")
            
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
