# 🪟 WindowScope v2.1

一个功能强大、UI现代的 Windows 窗口实时监视工具。

[![Version](https://img.shields.io/badge/version-2.1.0-blue.svg)](https://github.com/yourusername/WindowScope)
[![Python](https://img.shields.io/badge/python-3.7+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![Architecture](https://img.shields.io/badge/architecture-modular-orange.svg)]()
[![UI](https://img.shields.io/badge/UI-modern-purple.svg)]()

## ✨ 核心特性

- 🎯 **图形化区域选择** - 在截图上拖拽选择监视区域，所见即所得
- 📺 **实时视频流** - 以 1-60 FPS 帧率实时监视窗口内容
- 🔄 **多种捕获方法** - 自动尝试 win32ui、PrintWindow 等方法
- ⚡ **动态帧率调节** - 运行时调整刷新率，平衡性能与流畅度
- 🪟 **窗口置顶显示** - 监视窗口始终保持在最前面
- 🎨 **现代化UI设计** - 深色主题、渐变按钮、卡片布局，企业级视觉体验
- 🏗️ **模块化架构** - 采用分层架构，遵循 SOLID 原则

## 🎨 UI 设计特点

- **深色主题** - 专业的深蓝黑配色（#0F172A），护眼且时尚
- **渐变按钮** - 绿色/蓝色渐变，视觉吸引力强
- **卡片布局** - 分组化设计，逻辑清晰易懂
- **无边框窗口** - 监视窗口采用圆角无边框设计
- **视觉反馈** - 悬停、按下、禁用等完整交互反馈
- **淡入动画** - 平滑的窗口显示动画

**UI现代化程度**: 94% | 详见 [UI现代化报告](docs/archive/UI现代化完成报告.md)

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行程序

**方式 1：双击启动脚本**（最简单）
```bash
run_new_version.bat
```

**方式 2：命令行启动**
```bash
python -m src.main
```

**方式 3：从 src 目录启动**
```bash
cd src
python main.py
```

### 基本使用

1. 📝 **打开测试窗口**：打开记事本、浏览器等任意窗口
2. 🎯 **选择窗口**：在下拉列表中选择要监视的窗口
3. ✂️ **选择区域**：点击"图形化选择区域"，拖拽鼠标选择监视范围
4. 🚀 **启动监视**：点击"启动监视"按钮，实时画面立即呈现

详细使用说明请查看 [快速启动指南](docs/快速启动指南_新架构.md)

## 📁 项目结构

```
WindowScope/
├── README.md            # 项目主文档
├── requirements.txt     # Python 依赖
├── run_new_version.bat  # 启动脚本
├── LICENSE              # MIT 许可证
├── .gitignore           # Git 配置
│
├── src/                 # 源代码（模块化架构）
│   ├── config/          # 配置管理（settings + theme）
│   ├── core/            # 核心业务逻辑
│   ├── ui/              # 用户界面（现代化设计）
│   ├── utils/           # 工具模块
│   └── main.py          # 程序入口
│
├── docs/                # 完整文档
│   ├── 快速启动指南_新架构.md
│   ├── 项目架构说明.md
│   ├── UI现代化完成报告.md
│   └── ...更多文档
│
└── tests/               # 测试文件
    └── test_import.py
```

详细结构请查看 [项目结构说明](docs/PROJECT_STRUCTURE.md)

## 🏗️ 架构特点

### 模块化架构 v2.1

- ✅ **分层架构** - Config → Utils → Core → UI，职责清晰
- ✅ **信号驱动** - 使用 PyQt6 信号/槽机制实现解耦
- ✅ **SOLID 原则** - 单一职责、开闭原则、依赖倒置等
- ✅ **配置管理** - 集中配置，易于维护和扩展
- ✅ **专业日志** - 完整的日志系统，支持控制台和文件输出
- ✅ **易于测试** - 独立的模块，方便单元测试

### 现代化UI设计 v2.1

- ✅ **深色主题** - 专业的深蓝色配色方案，护眼且时尚
- ✅ **渐变效果** - 启动按钮和选择按钮采用渐变设计
- ✅ **卡片布局** - 分组化布局，逻辑清晰易懂
- ✅ **无边框设计** - 监视窗口采用现代无边框圆角设计
- ✅ **视觉反馈** - 所有交互都有悬停、按下等视觉反馈
- ✅ **动画效果** - 平滑的窗口淡入动画

详细说明请查看 [项目架构文档](docs/项目架构说明.md) | [UI现代化报告](docs/archive/UI现代化完成报告.md)

## 📖 文档

### 🚀 快速开始
- 📘 [快速启动指南](docs/快速启动指南_新架构.md) - 5 分钟快速上手 ⭐
- 📦 [打包指南](docs/packaging-guide/) - 将程序打包为 exe 文件 ⭐

### 📚 核心文档
- 📗 [项目架构说明](docs/项目架构说明.md) - 深入理解架构设计
- 📕 [完整功能文档](docs/README_新架构.md) - 详细使用手册
- 📙 [项目结构说明](docs/PROJECT_STRUCTURE.md) - 目录结构导航
- 🔧 [问题修复记录](docs/问题修复记录.md) - 已知问题和解决方案

### 📜 历史文档
所有历史报告和记录已移至 [docs/archive/](docs/archive/)：
- 架构迁移和重构报告
- UI 现代化改进报告
- 项目完成总结

**查看所有文档**: [📚 文档中心](docs/README.md) ← 完整文档导航

## 🔧 配置选项

主要配置位于 `src/config/settings.py` 和 `src/config/theme.py`：

```python
# 捕获设置
default_fps = 30          # 默认帧率
min_fps = 1               # 最小帧率
max_fps = 60              # 最大帧率

# UI 设置
main_window_width = 520   # 主窗口宽度
selector_max_width = 1200 # 选择器最大宽度

# 主题颜色（深色模式）
primary = '#2563EB'       # 现代蓝
success = '#10B981'       # 翠绿
background = '#0F172A'    # 深蓝黑
```

## 🧪 测试

运行导入测试：
```bash
python tests/test_import.py
```

预期输出：
```
[SUCCESS] All modules imported successfully!
```

## 📊 性能

| 场景 | 推荐帧率 | CPU 占用 |
|------|---------|---------|
| 文本编辑器 | 5-10 FPS | 很低 |
| 网页浏览 | 15-20 FPS | 中等 |
| 视频播放 | 30 FPS | 中高 |
| 游戏监视 | 30-60 FPS | 高 |

## 📁 根目录文件

保持简洁，只包含核心文件：

```
WindowScope/
├── README.md            # 本文件
├── requirements.txt     # Python 依赖
├── run_new_version.bat  # 启动脚本
├── LICENSE              # 开源许可证
├── .gitignore           # Git 配置
├── src/                 # 源代码（模块化架构）
├── docs/                # 完整文档
└── tests/               # 测试文件
```

详细结构请查看 [项目结构说明](docs/PROJECT_STRUCTURE.md)

## ⚠️ 注意事项

- ✅ 目标窗口不能被最小化（Windows API 限制）
- ✅ 某些受保护的窗口可能无法捕获（如 DRM 内容）
- ✅ 大窗口或高帧率会增加 CPU 占用

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

开发规范：
- 遵循 PEP 8 代码风格
- 使用类型提示
- 编写文档字符串
- 遵循 SOLID 原则
- 保持UI一致性

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🎓 技术栈

- **Python 3.7+**
- **PyQt6** - GUI 框架
- **pywin32** - Windows API 接口
- **dataclasses** - 配置管理
- **logging** - 日志系统

## 🌟 项目亮点

### 技术层面
- ✅ 模块化架构设计
- ✅ SOLID 原则应用
- ✅ 设计模式实践
- ✅ 信号驱动编程
- ✅ 专业日志系统

### 视觉层面
- ✅ 现代化UI设计
- ✅ 深色主题系统
- ✅ 统一样式管理
- ✅ 优雅的动画效果
- ✅ 完整的视觉反馈

### 工程层面
- ✅ 完整的文档体系
- ✅ 标准化项目结构
- ✅ 清晰的代码组织
- ✅ 易于扩展维护

## 📮 联系方式

- Issues: [GitHub Issues](https://github.com/yourusername/WindowScope/issues)

---

**版本**: 2.1.0 | **最后更新**: 2025-10-29 | **架构**: 模块化 + SOLID + 现代UI

**立即体验**: 双击 `run_new_version.bat` 🚀
