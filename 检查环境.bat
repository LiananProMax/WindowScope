@echo off
chcp 65001 >nul 2>nul
echo ========================================
echo 环境诊断工具
echo ========================================
echo.

echo [1/6] 检查 Python...
where python >nul 2>nul
if errorlevel 1 (
    echo [失败] 未找到 Python
    echo 请安装 Python 并添加到 PATH
    set HAS_ERROR=1
) else (
    python --version
    echo [成功] Python 可用
)
echo.

echo [2/6] 检查 pip...
where pip >nul 2>nul
if errorlevel 1 (
    echo [失败] 未找到 pip
    set HAS_ERROR=1
) else (
    pip --version
    echo [成功] pip 可用
)
echo.

echo [3/6] 检查项目文件...
if exist "src\main.py" (
    echo [成功] 找到 src\main.py
) else (
    echo [失败] 未找到 src\main.py
    echo 当前目录: %CD%
    set HAS_ERROR=1
)

if exist "requirements.txt" (
    echo [成功] 找到 requirements.txt
) else (
    echo [失败] 未找到 requirements.txt
    set HAS_ERROR=1
)

if exist "build_exe.spec" (
    echo [成功] 找到 build_exe.spec
) else (
    echo [失败] 未找到 build_exe.spec
    set HAS_ERROR=1
)
echo.

echo [4/6] 检查依赖包...
python -c "import PyQt6" 2>nul
if errorlevel 1 (
    echo [失败] 未安装 PyQt6
    echo 运行: pip install PyQt6
    set HAS_ERROR=1
) else (
    echo [成功] PyQt6 已安装
)

python -c "import win32api" 2>nul
if errorlevel 1 (
    echo [失败] 未安装 pywin32
    echo 运行: pip install pywin32
    set HAS_ERROR=1
) else (
    echo [成功] pywin32 已安装
)

python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [提示] 未安装 PyInstaller（打包时会自动安装）
) else (
    echo [成功] PyInstaller 已安装
)
echo.

echo [5/6] 检查程序是否能正常运行...
python -c "from src.main import main; print('[成功] 程序导入正常')" 2>nul
if errorlevel 1 (
    echo [失败] 程序导入失败，可能有语法错误或缺少依赖
    set HAS_ERROR=1
) else (
    echo [成功] 程序可以正常导入
)
echo.

echo [6/6] 诊断总结
echo ========================================
if defined HAS_ERROR (
    echo.
    echo [结果] 发现问题！请修复上述标记为 [失败] 的项目
    echo.
    echo 快速修复命令：
    echo    pip install -r requirements.txt
    echo    pip install pyinstaller
    echo.
) else (
    echo.
    echo [结果] 环境检查通过！可以开始打包了。
    echo.
    echo 运行打包：双击 build_exe.bat
    echo.
)
echo ========================================
echo.
pause

