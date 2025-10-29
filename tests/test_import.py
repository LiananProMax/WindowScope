#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试新架构是否可以正常导入"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("Testing new architecture imports...")
print("-" * 60)

try:
    from src.config import settings
    print("[OK] Config module imported successfully")
    print(f"     Version: {settings.version}")
    print(f"     FPS range: {settings.capture.min_fps}-{settings.capture.max_fps}")
except Exception as e:
    print(f"[FAIL] Config module: {e}")
    sys.exit(1)

try:
    from src.utils import logger
    print("[OK] Logger module imported successfully")
    logger.info("Logger test message")
except Exception as e:
    print(f"[FAIL] Logger module: {e}")
    sys.exit(1)

try:
    from src.utils import WindowManager, ScreenCapture
    print("[OK] Windows utility module imported successfully")
except Exception as e:
    print(f"[FAIL] Windows utility module: {e}")
    sys.exit(1)

try:
    from src.core import CaptureEngine
    print("[OK] Capture engine module imported successfully")
except Exception as e:
    print(f"[FAIL] Capture engine module: {e}")
    sys.exit(1)

try:
    from src.ui import RegionSelector, CaptureWindow, MainWindow
    print("[OK] UI modules imported successfully")
except Exception as e:
    print(f"[FAIL] UI modules: {e}")
    sys.exit(1)

print("-" * 60)
print("[SUCCESS] All modules imported successfully!")
print("You can now run: python -m src.main")

