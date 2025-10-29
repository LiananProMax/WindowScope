# WindowScope 打包说明

## 一键打包

**最简单的方式：双击运行**

```
build.bat
```

## 打包步骤

脚本会自动完成以下步骤：

1. **环境检查**
   - 检查 Python 是否安装
   - 检查项目文件是否完整
   - 验证 build_exe.spec 配置文件

2. **安装依赖**
   - 自动安装 PyQt6
   - 自动安装 pywin32
   - 自动安装 PyInstaller

3. **验证源代码**
   - 检查最小化窗口检测功能
   - 检查主窗口最小化处理
   - 检查捕获引擎最小化检测

4. **清理缓存**
   - 清理 Python 字节码 (__pycache__, *.pyc)
   - 清理旧的 build 和 dist 目录
   - 清理 PyInstaller 缓存

5. **打包程序**
   - 使用 PyInstaller 打包
   - 生成单文件 exe
   - 验证打包结果

## 输出

成功后会生成：
- `dist\WindowScope.exe` - 可执行文件（约 40MB）

## 时间

整个过程需要 **2-5 分钟**，取决于：
- 电脑性能
- 网络速度（首次安装依赖时）
- 杀毒软件（可能会扫描）

## 常见问题

### 问题：打包失败
**解决方案：**
```bash
# 手动安装依赖
pip install -r requirements.txt
pip install pyinstaller

# 再次运行打包
build.bat
```

### 问题：杀毒软件报警
**解决方案：**
- 暂时关闭杀毒软件
- 或者将项目目录加入白名单

### 问题：权限不足
**解决方案：**
- 右键 build.bat → 以管理员身份运行

## 测试打包后的程序

运行生成的 exe：
```
dist\WindowScope.exe
```

测试功能：
1. 选择一个最小化的窗口
2. 点击"图形化选择区域" - 应该自动恢复窗口
3. 点击"启动监视" - 应该检查窗口是否最小化

## 手动打包（高级）

如果需要自定义打包选项：

```bash
# 清理缓存
rd /s /q build dist

# 自定义打包
pyinstaller build_exe.spec --clean
```

查看 `build_exe.spec` 文件进行更多配置。

