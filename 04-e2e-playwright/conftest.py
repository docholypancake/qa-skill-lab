"""Root conftest for Module 04.

Adds the module root to sys.path so `from pages.x import X` works
both in CLI (pytest.ini pythonpath) and in the VSCode test extension
(which doesn't read pytest.ini pythonpath reliably).
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
