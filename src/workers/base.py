import traceback
import sys
from typing import Callable, Any

from PySide6.QtCore import QRunnable, Slot, Signal, QObject

class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.
    """
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)

class BaseWorker(QRunnable):
    """
    Worker thread foundation for long-running background tasks.
    Inherits from QRunnable to handle worker thread setup, signals and wrap-up.
    """
    def __init__(self, fn: Callable, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        """
        Initialize the runner function with passed args, kwargs.
        """
        try:
            # Pass progress callback if needed by the function
            # self.kwargs['progress_callback'] = self.signals.progress
            result = self.fn(*self.args, **self.kwargs)
        except Exception:
            traceback.print_exc()
            exctype, value = sys.exc_info()
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()
