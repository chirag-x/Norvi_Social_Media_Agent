from PySide6.QtCore import QObject, Signal
from typing import Optional
from src.discovery.provider import VideoResult

class AppState(QObject):
    """
    Centralized runtime state for the application.
    """
    active_source_changed = Signal(object) # Emits VideoResult or None

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = AppState()
        return cls._instance

    def __init__(self):
        super().__init__()
        self._active_source: Optional[VideoResult] = None
        self.transcript = None
        self.extracted_clips = None

    @property
    def active_source(self) -> Optional[VideoResult]:
        return self._active_source

    @active_source.setter
    def active_source(self, video: Optional[VideoResult]):
        self._active_source = video
        self.active_source_changed.emit(video)
