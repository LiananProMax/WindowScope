@echo off
chcp 65001 >nul
echo ========================================
echo 实时窗口监视器 v2.1 - 新架构版本
echo ========================================
echo.
echo 正在启动...
echo.

cd /d "%~dp0"
python -m src.main

pause

