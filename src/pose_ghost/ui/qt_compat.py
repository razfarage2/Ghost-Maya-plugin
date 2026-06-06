# src/pose_ghost/ui/qt_compat.py
import sys

HAS_PYSIDE6 = False
HAS_PYSIDE2 = False
QT_AVAILABLE = False
IMPORT_ERROR_MSG = ""

QtCore = None
QtWidgets = None
QtGui = None

try:
    from PySide6 import QtCore, QtWidgets, QtGui
    HAS_PYSIDE6 = True
    QT_AVAILABLE = True
except ImportError as e6:
    try:
        from PySide2 import QtCore, QtWidgets, QtGui
        HAS_PYSIDE2 = True
        QT_AVAILABLE = True
    except ImportError as e2:
        IMPORT_ERROR_MSG = f"Neither PySide6 nor PySide2 is available.\nPySide6 error: {e6}\nPySide2 error: {e2}"

def ensure_qt_available():
    """Raises an error if Qt is not available."""
    if not QT_AVAILABLE:
        raise RuntimeError(f"Qt bindings not found. {IMPORT_ERROR_MSG}")

__all__ = [
    "QtCore",
    "QtWidgets",
    "QtGui",
    "HAS_PYSIDE6",
    "HAS_PYSIDE2",
    "QT_AVAILABLE",
    "ensure_qt_available"
]