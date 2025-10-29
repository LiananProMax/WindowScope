# 🪟 WindowScope v2.1 - 架构重构版

## 📋 项目概述

这是一个基于现代软件工程原则重构的 Windows 窗口实时监视工具，采用模块化、面向对象的架构设计。

## ✨ 架构亮点

### 🏗️ 模块化设计
```
src/
├── config/      # 配置管理
├── core/        # 核心业务逻辑
├── ui/          # 用户界面
└── utils/       # 工具模块
```

### 🎨 设计模式
- ✅ **单例模式** - Logger, Settings
- ✅ **观察者模式** - 信号/槽机制
- ✅ **依赖注入** - 解耦组件
- ✅ **工厂模式** - 多种捕获方法
- ✅ **策略模式** - 配置驱动

### 📐 SOLID 原则
- ✅ **S** - 单一职责
- ✅ **O** - 开闭原则
- ✅ **L** - 里氏替换
- ✅ **I** - 接口隔离
- ✅ **D** - 依赖倒置

## 📁 目录结构

```
WindowScope/
├── src/
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py          # ✅ 已完成 - 配置管理
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   └── capture_engine.py    # ✅ 已完成 - 捕获引擎
│   │
│   ├── ui/
│   │   ├── __init__.py          # ⏳ 待创建
│   │   ├── region_selector.py  # ✅ 已完成 - 区域选择器
│   │   ├── capture_window.py   # ⏳ 需要迁移
│   │   └── main_window.py       # ⏳ 需要迁移
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py            # ✅ 已完成 - 日志管理
│   │   └── win32_helper.py      # ✅ 已完成 - Windows API
│   │
│   ├── __init__.py              # ✅ 已完成
│   └── main.py                  # ⏳ 待创建 - 程序入口
│
├── window_capture_pyqt6.py      # 旧版本（备份）
├── requirements.txt             # ⏳ 待创建
├── README_新架构.md             # 本文件
├── 项目架构说明.md              # 详细架构文档
├── 架构重构完成报告.md          # 完成报告
└── 下一步行动清单.md            # 操作指南
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install pywin32 PyQt6
```

### 2. 运行程序

**选项 A**: 使用新架构（完成迁移后）
```bash
cd C:\Users\user\EVE\EVE-window-capture
python -m src.main
```

**选项 B**: 使用旧版本（当前可用）
```bash
python window_capture_pyqt6.py
```

## 📊 架构对比

### 旧架构 (单文件)
```
window_capture_pyqt6.py (981行)
├─ 全局函数
├─ 数据结构
├─ UI 类 + 业务逻辑
└─ 混在一起
```
**问题**: 耦合高、难测试、难维护

### 新架构 (模块化)
```
src/ (多文件)
├─ config/    (配置层)
├─ core/      (业务层)
├─ ui/        (展示层)
└─ utils/     (工具层)
```
**优势**: 解耦、易测试、易维护

## 🎯 核心组件

### 1. 配置管理 (`config/settings.py`)

```python
@dataclass
class AppSettings:
    app_name: str = "实时窗口监视器"
    version: str = "2.1.0"
    capture: CaptureSettings = ...
    ui: UISettings = ...
    debug: DebugSettings = ...

# 全局配置
settings = AppSettings()
```

### 2. 日志管理 (`utils/logger.py`)

```python
from ..utils import logger

logger.info("应用启动")
logger.debug("调试信息")
logger.error("错误信息")
```

### 3. Windows 工具 (`utils/win32_helper.py`)

```python
# 窗口管理
windows = WindowManager.enum_windows()
title = WindowManager.get_window_title(hwnd)

# 屏幕捕获
img, method = ScreenCapture.capture_window(hwnd, width, height)
```

### 4. 捕获引擎 (`core/capture_engine.py`)

```python
engine = CaptureEngine(hwnd, region, fps=30)

# 连接信号
engine.frame_captured.connect(on_frame)
engine.fps_updated.connect(on_fps_update)

# 控制
engine.start()
engine.pause()
engine.set_fps(60)
```

### 5. UI 组件 (`ui/`)

```python
# 区域选择器
selector = RegionSelector(screenshot, width, height)
if selector.exec():
    region = selector.get_selected_region()

# 监视窗口
window = CaptureWindow(engine, title)
window.show()

# 主窗口
main = MainWindow()
main.show()
```

## 📝 开发指南

### 添加新功能

1. **新的捕获方法**
```python
# 在 utils/win32_helper.py
class ScreenCapture:
    @staticmethod
    def capture_window_new_method(...):
        ...
```

2. **新的配置选项**
```python
# 在 config/settings.py
@dataclass
class NewSettings:
    option: bool = True
```

3. **新的 UI 组件**
```python
# 在 ui/new_component.py
class NewComponent(QWidget):
    ...
```

### 调试技巧

```python
# 启用详细日志
settings.debug.enabled = True

# 启用文件日志
settings.debug.log_to_file = True
logger.add_file_handler("debug.log")

# 查看配置
print(settings.capture.default_fps)
```

## 🧪 测试

### 单元测试示例

```python
def test_capture_engine():
    engine = CaptureEngine(hwnd=12345, region=(0,0,100,100))
    assert engine.fps == 30

def test_window_manager():
    windows = WindowManager.enum_windows()
    assert len(windows) > 0
```

### 集成测试

```python
def test_full_workflow():
    app = QApplication([])
    main = MainWindow()
    # 模拟用户操作
    ...
```

## 📈 性能优化

### 配置调优

```python
# 低性能设备
settings.capture.default_fps = 15

# 高性能设备
settings.capture.default_fps = 60
```

### 日志优化

```python
# 生产环境关闭调试日志
settings.debug.enabled = False
```

## 🔧 配置选项

### 捕获设置

```python
settings.capture.default_fps = 30      # 默认帧率
settings.capture.min_fps = 1           # 最小帧率
settings.capture.max_fps = 60          # 最大帧率
settings.capture.min_region_size = 10  # 最小区域尺寸
```

### UI 设置

```python
settings.ui.main_window_width = 450
settings.ui.main_window_height = 350
settings.ui.selector_max_width = 1200
settings.ui.selector_max_height = 800
```

### 调试设置

```python
settings.debug.enabled = True
settings.debug.verbose_interval = 30  # 详细输出间隔
settings.debug.log_to_file = False
```

## 📚 文档

- **项目架构说明.md** - 详细的架构设计文档
- **架构重构完成报告.md** - 重构过程和成果
- **下一步行动清单.md** - 完成剩余工作的指南

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 开发规范

1. 遵循 PEP 8 代码风格
2. 使用类型提示
3. 编写文档字符串
4. 添加单元测试
5. 更新文档

## 📄 许可证

MIT License

## 🎉 致谢

感谢所有贡献者和用户！

---

**版本**: 2.1.0  
**最后更新**: 2025-10-29  
**架构**: 模块化 + SOLID 原则 + 现代软件工程实践

