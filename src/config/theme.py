"""
主题配置模块
定义现代化的色彩系统
"""


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
    
    @classmethod
    def get_theme(cls, theme_name='dark'):
        """获取指定主题"""
        return cls.DARK if theme_name == 'dark' else cls.LIGHT

