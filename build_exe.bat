@echo off
chcp 65001 >nul 2>nul
echo ========================================
echo WindowScope - 打包为 EXE
echo ========================================
echo.

REM 检查 Python 是否可用
echo [检查] 正在检查 Python 环境...
where python >nul 2>nul
if errorlevel 1 (
    echo [错误] 未找到 Python！
    echo.
    echo 请确保：
    echo 1. 已安装 Python 3.8 或更高版本
    echo 2. Python 已添加到系统 PATH 环境变量
    echo.
    echo 安装 Python: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM 显示 Python 版本
for /f "delims=" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [成功] 检测到 %PYTHON_VERSION%
echo.

REM 检查是否在正确的目录
if not exist "src\main.py" (
    echo [错误] 未找到 src\main.py 文件！
    echo 请确保在项目根目录运行此脚本。
    echo 当前目录: %CD%
    echo.
    pause
    exit /b 1
)

REM 检查是否安装了 PyInstaller
echo [检查] 正在检查 PyInstaller...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [提示] 未检测到 PyInstaller，正在安装...
    echo.
    pip install pyinstaller
    if errorlevel 1 (
        echo.
        echo [错误] 安装 PyInstaller 失败！
        echo.
        echo 请尝试手动安装：
        echo    pip install pyinstaller
        echo.
        echo 或者使用国内镜像：
        echo    pip install pyinstaller -i https://pypi.tuna.tsinghua.edu.cn/simple
        echo.
        pause
        exit /b 1
    )
    echo.
    echo [成功] PyInstaller 安装成功！
    echo.
) else (
    echo [成功] PyInstaller 已安装
    echo.
)

echo [1/3] 清理旧的构建文件...
if exist "build" rd /s /q "build"
if exist "dist" rd /s /q "dist"
echo 完成！
echo.

echo [2/3] 开始打包程序...
echo 这可能需要几分钟时间，请耐心等待...
echo.

REM 运行打包命令
pyinstaller build_exe.spec --clean

if errorlevel 1 (
    echo.
    echo ========================================
    echo [错误] 打包失败！
    echo ========================================
    echo.
    echo 请查看上方的错误信息。
    echo.
    echo 常见问题：
    echo 1. 缺少依赖包 - 运行: pip install -r requirements.txt
    echo 2. 权限不足 - 尝试以管理员身份运行
    echo 3. 杀毒软件拦截 - 暂时关闭杀毒软件
    echo 4. PyQt6 未安装 - 运行: pip install PyQt6
    echo 5. pywin32 未安装 - 运行: pip install pywin32
    echo.
    pause
    exit /b 1
)

echo.
echo [3/3] 打包完成！
echo.
echo ========================================
echo 打包成功！
echo ========================================
echo.
echo 生成的 EXE 文件位于: dist\WindowScope.exe
echo.
echo 你可以直接运行这个 exe 文件，无需安装 Python！
echo.

REM 询问是否打开文件夹
echo 是否打开输出文件夹？(Y/N)
choice /c YN /n /m "请选择: "
if errorlevel 2 goto end
if errorlevel 1 explorer dist

:end
echo.
pause

