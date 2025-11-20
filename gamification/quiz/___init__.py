from pathlib import Path
import importlib
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]  # /.../gamification
PROJECT_ROOT = ROOT_DIR.parent

project_root_str = str(PROJECT_ROOT)
if project_root_str not in sys.path:
    sys.path.insert(0, project_root_str)

quiz_module = importlib.import_module("quiz")
quiz_module.__name__ = __name__
sys.modules[__name__] = quiz_module