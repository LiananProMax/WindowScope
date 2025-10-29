# 📁 项目结构

```
WindowScope/
│
├── 📄 README.md                    # 项目主文档（你正在这里）
├── 📄 PROJECT_STRUCTURE.md         # 项目结构说明（本文件）
├── 📄 requirements.txt             # Python 依赖
├── 🚀 run_new_version.bat         # 启动脚本
├── 📄 window_capture_pyqt6.py     # 旧版本（单文件，备份）
│
├── 📂 src/                         # 新架构源代码
│   ├── 📄 __init__.py
│   ├── 🎯 main.py                 # 程序入口
│   │
│   ├── 📂 config/                 # 配置管理
│   │   ├── __init__.py
│   │   └── settings.py            # 集中配置
│   │
│   ├── 📂 core/                   # 核心业务逻辑
│   │   ├── __init__.py
│   │   └── capture_engine.py     # 捕获引擎
│   │
│   ├── 📂 ui/                     # 用户界面
│   │   ├── __init__.py
│   │   ├── main_window.py        # 主窗口
│   │   ├── capture_window.py     # 监视窗口
│   │   └── region_selector.py    # 区域选择器
│   │
│   └── 📂 utils/                  # 工具模块
│       ├── __init__.py
│       ├── logger.py              # 日志管理
│       └── win32_helper.py        # Windows API
│
├── 📂 docs/                        # 文档目录
│   ├── 📄 README.md               # 文档索引
│   ├── 📄 快速启动指南_新架构.md
│   ├── 📄 项目架构说明.md
│   ├── 📄 迁移完成报告.md
│   ├── 📄 README_新架构.md
│   ├── 📄 架构重构完成报告.md
│   ├── 📄 下一步行动清单.md
│   └── 📄 架构迁移成功.txt
│
└── 📂 tests/                       # 测试文件
    └── test_import.py             # 导入测试
```

## 📊 文件统计

| 类型 | 数量 | 说明 |
|------|------|------|
| 📄 Python 源文件 | 13 | 模块化设计 |
| 📄 文档文件 | 8 | 完整文档体系 |
| 🧪 测试文件 | 1 | 导入测试 |
| 🚀 启动脚本 | 1 | 快速启动 |

## 🎯 目录职责

### src/ - 源代码目录

**config/** - 配置层
- 集中管理所有配置项
- 使用 dataclass 实现类型安全
- 易于维护和扩展

**core/** - 核心业务逻辑层
- CaptureEngine: 捕获引擎
- 信号驱动架构
- 与 UI 完全解耦

**ui/** - 用户界面层
- MainWindow: 主窗口
- CaptureWindow: 监视窗口
- RegionSelector: 区域选择器
- 只负责展示和用户交互

**utils/** - 工具层
- Logger: 日志管理
- WindowManager: 窗口管理
- ScreenCapture: 屏幕捕获
- 封装底层 API

### docs/ - 文档目录

包含所有项目文档，保持根目录整洁。

### tests/ - 测试目录

包含测试脚本和测试数据。

## 🔗 依赖关系

```
UI 层 (ui/)
  ↓ 使用
Core 层 (core/)
  ↓ 调用
Utils 层 (utils/)
  ↓ 读取
Config 层 (config/)
```

## 📝 文件说明

### 根目录核心文件

- **README.md**: 项目主文档，包含快速开始、功能介绍
- **requirements.txt**: Python 依赖列表
- **run_new_version.bat**: Windows 启动脚本
- **window_capture_pyqt6.py**: 旧版本单文件实现（备份）

### 源代码核心文件

- **main.py**: 程序入口，初始化应用
- **settings.py**: 配置管理，集中配置项
- **capture_engine.py**: 核心捕获引擎
- **logger.py**: 日志系统
- **win32_helper.py**: Windows API 封装

## 🎓 设计原则

1. **模块化**: 按职责划分模块
2. **分层**: 清晰的层次结构
3. **解耦**: 使用信号/槽机制
4. **配置化**: 集中配置管理
5. **文档化**: 完整的文档体系

## 📦 打包结构

如果需要打包发布：

```
WindowScope-v2.1.0/
├── src/
├── docs/
├── README.md
├── requirements.txt
└── run_new_version.bat
```

## 🔄 版本对比

| 版本 | 文件结构 | 代码行数 | 维护性 |
|------|---------|---------|--------|
| v1.0 | 1 个文件 | 982 行 | 低 |
| v2.1 | 13 个模块 | ~1,324 行 | 高 |

---

返回 [主 README](README.md) | 查看 [文档索引](docs/README.md)

