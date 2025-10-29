@echo off
chcp 65001 >nul 2>nul
cls
echo ========================================
echo WindowScope - Complete Build Tool
echo ========================================
echo.
echo This script will:
echo   1. Check and fix environment
echo   2. Install missing dependencies
echo   3. Verify source code
echo   4. Clean cache
echo   5. Build EXE package
echo.
pause

REM ============================================
REM Step 1: Environment Check and Fix
REM ============================================
echo.
echo ========================================
echo [1/5] Environment Check
echo ========================================
echo.

set HAS_ERROR=0

echo Checking Python...
where python >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)
python --version
echo OK: Python found

echo.
echo Checking project directory...
if not exist "src\main.py" (
    echo ERROR: src\main.py not found
    echo Current directory: %CD%
    echo Please run this script in project root
    pause
    exit /b 1
)
echo OK: Project files found

echo.
echo Checking build_exe.spec...
if not exist "build_exe.spec" (
    echo ERROR: build_exe.spec not found
    pause
    exit /b 1
)
echo OK: Spec file found

REM ============================================
REM Step 2: Install Dependencies
REM ============================================
echo.
echo ========================================
echo [2/5] Install Dependencies
echo ========================================
echo.

echo Checking PyQt6...
python -c "import PyQt6" 2>nul
if errorlevel 1 (
    echo Installing PyQt6...
    pip install PyQt6
    if errorlevel 1 (
        echo ERROR: Failed to install PyQt6
        set HAS_ERROR=1
    ) else (
        echo OK: PyQt6 installed
    )
) else (
    echo OK: PyQt6 already installed
)

echo.
echo Checking pywin32...
python -c "import win32api" 2>nul
if errorlevel 1 (
    echo Installing pywin32...
    pip install pywin32
    if errorlevel 1 (
        echo ERROR: Failed to install pywin32
        set HAS_ERROR=1
    ) else (
        echo OK: pywin32 installed
    )
) else (
    echo OK: pywin32 already installed
)

echo.
echo Checking PyInstaller...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller
        set HAS_ERROR=1
    ) else (
        echo OK: PyInstaller installed
    )
) else (
    echo OK: PyInstaller already installed
)

if %HAS_ERROR%==1 (
    echo.
    echo ERROR: Some dependencies failed to install
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

REM ============================================
REM Step 3: Verify Source Code
REM ============================================
echo.
echo ========================================
echo [3/5] Verify Source Code
echo ========================================
echo.

set CODE_ERROR=0

echo Checking minimize detection in win32_helper...
findstr /C:"is_window_minimized" src\utils\win32_helper.py >nul 2>nul
if errorlevel 1 (
    echo ERROR: Missing is_window_minimized function
    set CODE_ERROR=1
) else (
    echo OK: Minimize detection found
)

echo.
echo Checking minimize handler in main_window...
findstr /C:"was_minimized" src\ui\main_window.py >nul 2>nul
if errorlevel 1 (
    echo ERROR: Missing minimize handler
    set CODE_ERROR=1
) else (
    echo OK: Minimize handler found
)

echo.
echo Checking minimize detection in capture_engine...
findstr /C:"WindowManager.is_window_minimized" src\core\capture_engine.py >nul 2>nul
if errorlevel 1 (
    echo ERROR: Missing minimize detection in engine
    set CODE_ERROR=1
) else (
    echo OK: Engine minimize detection found
)

if %CODE_ERROR%==1 (
    echo.
    echo ERROR: Source code verification failed
    echo Please make sure all changes are saved
    pause
    exit /b 1
)

echo.
echo OK: All source code verified

REM ============================================
REM Step 4: Clean Cache
REM ============================================
echo.
echo ========================================
echo [4/5] Clean Cache
echo ========================================
echo.

echo Cleaning Python bytecode cache...
for /d /r %%d in (__pycache__) do @if exist "%%d" (
    echo Removing: %%d
    rd /s /q "%%d" 2>nul
)
for /r %%f in (*.pyc) do @if exist "%%f" (
    del /q "%%f" 2>nul
)
echo OK: Python cache cleaned

echo.
echo Cleaning build directories...
if exist "build" (
    echo Removing: build
    rd /s /q "build" 2>nul
)
if exist "dist" (
    echo Removing: dist
    rd /s /q "dist" 2>nul
)
echo OK: Build directories cleaned

echo.
echo Cleaning PyInstaller cache...
if exist "%TEMP%\pyinstaller" (
    rd /s /q "%TEMP%\pyinstaller" 2>nul
)
if exist "%LOCALAPPDATA%\pyinstaller" (
    rd /s /q "%LOCALAPPDATA%\pyinstaller" 2>nul
)
echo OK: PyInstaller cache cleaned

REM ============================================
REM Step 5: Build Package
REM ============================================
echo.
echo ========================================
echo [5/5] Build Package
echo ========================================
echo.
echo Starting PyInstaller...
echo This will take 2-5 minutes, please wait...
echo.
echo ----------------------------------------

pyinstaller build_exe.spec --clean

echo ----------------------------------------
echo.

if errorlevel 1 (
    echo.
    echo ========================================
    echo ERROR: Build Failed!
    echo ========================================
    echo.
    echo The build process encountered an error.
    echo Please check the output above for details.
    echo.
    echo Common solutions:
    echo   1. Check internet connection
    echo   2. Run as administrator
    echo   3. Disable antivirus temporarily
    echo   4. Try: pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM ============================================
REM Verify Build Result
REM ============================================
echo.
echo ========================================
echo Verify Build Result
echo ========================================
echo.

if exist "dist\WindowScope.exe" (
    echo SUCCESS: WindowScope.exe created!
    echo.
    echo Location: dist\WindowScope.exe
    for %%F in ("dist\WindowScope.exe") do (
        echo File size: %%~zF bytes
        echo Modified: %%~tF
    )
    echo.
    echo ========================================
    echo Build Complete!
    echo ========================================
    echo.
    echo You can now run: dist\WindowScope.exe
    echo.
    echo Open output folder? (Y/N)
    choice /c YN /n /m "Select: "
    if errorlevel 1 if not errorlevel 2 explorer dist
) else (
    echo.
    echo WARNING: dist\WindowScope.exe not found!
    echo Build may have failed silently.
    echo.
    echo Please check:
    echo   1. Disk space available
    echo   2. Write permissions in this folder
    echo   3. PyInstaller output above for errors
    echo.
    if exist "dist" (
        echo dist folder exists, contents:
        dir dist
    ) else (
        echo dist folder was not created
    )
    echo.
    pause
)

echo.
echo ========================================
echo Script Complete
echo ========================================
pause
