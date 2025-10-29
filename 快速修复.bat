@echo off
chcp 65001 >nul 2>nul
echo ========================================
echo 快速修复依赖
echo ========================================
echo.

echo 正在安装所有必需的依赖包...
echo 这可能需要几分钟时间...
echo.

REM 检查 Python
where python >nul 2>nul
if errorlevel 1 (
    echo [错误] 未找到 Python！
    echo 请先安装 Python: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM 升级 pip
echo [1/3] 升级 pip...
python -m pip install --upgrade pip
echo.

REM 安装项目依赖
echo [2/3] 安装项目依赖 (PyQt6, pywin32)...
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [提示] 如果速度慢，可以使用国内镜像：
    echo pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    echo.
)
echo.

REM 安装 PyInstaller
echo [3/3] 安装 PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo.
    echo [提示] 如果速度慢，可以使用国内镜像：
    echo pip install pyinstaller -i https://pypi.tuna.tsinghua.edu.cn/simple
    echo.
)
echo.

echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 现在可以运行：
echo 1. 检查环境.bat - 验证安装
echo 2. build_exe.bat - 开始打包
echo.
pause

