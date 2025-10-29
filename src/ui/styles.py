"""
样式表管理模块
提供统一的UI样式
"""
from ..config.theme import ThemeColors


class StyleSheet:
    """统一样式表管理"""
    
    @staticmethod
    def get_stylesheet(theme='dark'):
        """
        获取完整样式表
        
        Args:
            theme: 主题名称 ('dark' 或 'light')
            
        Returns:
            str: 完整的样式表字符串
        """
        colors = ThemeColors.get_theme(theme)
        
        return f"""
        /* === 全局样式 === */
        * {{
            font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
        }}
        
        QMainWindow, QDialog {{
            background-color: {colors['background']};
            color: {colors['text_primary']};
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
        }}
        
        QPushButton:hover {{
            background-color: {colors['primary_hover']};
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
            font-size: 18px;
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
            padding: 8px 12px;
            font-size: 11px;
            min-height: 20px;
        }}
        
        QComboBox:focus {{
            border: 2px solid {colors['primary']};
        }}
        
        QComboBox:hover {{
            background-color: {colors['surface_hover']};
        }}
        
        QComboBox::drop-down {{
            border: none;
            padding-right: 8px;
        }}
        
        QComboBox QAbstractItemView {{
            background-color: {colors['surface']};
            color: {colors['text_primary']};
            border: 1px solid {colors['border']};
            selection-background-color: {colors['primary']};
            selection-color: white;
            padding: 4px;
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
        }}
        
        QSlider::sub-page:horizontal {{
            background-color: {colors['primary']};
            border-radius: 2px;
        }}
        
        /* === 分组框样式 === */
        QGroupBox {{
            color: {colors['text_primary']};
            border: 1px solid {colors['border']};
            border-radius: 8px;
            padding: 16px;
            margin-top: 12px;
            font-weight: 600;
            font-size: 13px;
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 12px;
            padding: 0 6px;
            background-color: {colors['background']};
        }}
        
        /* === 滚动条样式 === */
        QScrollBar:vertical {{
            background-color: {colors['background']};
            width: 10px;
            border: none;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {colors['surface_hover']};
            border-radius: 5px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {colors['border']};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
            background: none;
        }}
        """
    
    @staticmethod
    def get_button_primary():
        """获取主按钮样式"""
        return """
            QPushButton {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #10B981, stop: 1 #059669
                );
                color: white;
                font-size: 13px;
                font-weight: 700;
                border-radius: 6px;
                padding: 12px 24px;
                min-height: 44px;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #059669, stop: 1 #047857
                );
            }
            QPushButton:pressed {
                padding-top: 14px;
                padding-bottom: 10px;
            }
        """
    
    @staticmethod
    def get_button_secondary():
        """获取次要按钮样式"""
        return """
            QPushButton {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #2563EB, stop: 1 #1D4ED8
                );
                color: white;
                font-weight: 600;
                border-radius: 6px;
                padding: 10px 18px;
                min-height: 40px;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #1D4ED8, stop: 1 #1E40AF
                );
            }
        """

