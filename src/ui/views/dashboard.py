from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt
from src.workers.base import BaseWorker
from PySide6.QtCore import QThreadPool, Signal, QObject
from src.ai.ollama_manager import OllamaManager
from src.ai.model_manager import ModelManager
import asyncio

class DownloadSignals(QObject):
    progress = Signal(dict)
    finished = Signal(bool, str)

class DownloadWorker(BaseWorker):
    def __init__(self, target_coroutine, signals):
        super().__init__(target_coroutine)
        self.download_signals = signals
        
    def run(self):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.fn(self.download_signals))
            loop.close()
        except Exception as e:
            self.signals.error.emit((type(e), e, None))

class DashboardView(QWidget):
    """
    Dashboard view showing application overview.
    """
    def __init__(self):
        super().__init__()
        self.thread_pool = QThreadPool.globalInstance()
        self.ollama = OllamaManager.get_instance()
        self.model_mgr = ModelManager.get_instance()
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        title = QLabel("Dashboard")
        title.setProperty("class", "title")
        layout.addWidget(title)
        
        subtitle = QLabel("Welcome to Norvi Social Media Agent.\nSelect an option from the sidebar to begin.")
        subtitle.setProperty("class", "subtitle")
        layout.addWidget(subtitle)
        
        # System Status Box
        self.status_label = QLabel("Checking local AI runtime...")
        self.status_label.setProperty("class", "subtitle")
        self.status_label.setStyleSheet("margin-top: 20px; font-weight: bold;")
        layout.addWidget(self.status_label)
        
        # Model Status Box
        self.model_label = QLabel("Checking model status...")
        self.model_label.setProperty("class", "subtitle")
        layout.addWidget(self.model_label)
        
        self.btn_download_model = QPushButton("Download Required Model")
        self.btn_download_model.setProperty("class", "primary")
        self.btn_download_model.setFixedWidth(250)
        self.btn_download_model.hide()
        self.btn_download_model.clicked.connect(self.start_model_download)
        layout.addWidget(self.btn_download_model)
        
        from PySide6.QtWidgets import QProgressBar
        self.download_progress = QProgressBar()
        self.download_progress.setFixedWidth(400)
        self.download_progress.hide()
        layout.addWidget(self.download_progress)
        
        # Active Source Box
        self.active_source_label = QLabel("No active content source selected.")
        self.active_source_label.setProperty("class", "subtitle")
        self.active_source_label.setStyleSheet("margin-top: 20px;")
        layout.addWidget(self.active_source_label)
        
        from src.app.state import AppState
        AppState.get_instance().active_source_changed.connect(self._on_active_source_changed)
        
        layout.addStretch()
        self.setLayout(layout)
        
        # Initial check
        self.check_ai_status()
        
    def _on_active_source_changed(self, video):
        if video:
            self.active_source_label.setText(f"🎬 Active Source: {video.title}")
            self.active_source_label.setStyleSheet("margin-top: 20px; font-weight: bold; color: #3578FF;")
        else:
            self.active_source_label.setText("No active content source selected.")
            self.active_source_label.setStyleSheet("margin-top: 20px;")
        
        # Set up a Watchdog Timer to constantly monitor Ollama
        from PySide6.QtCore import QTimer
        self.watchdog_timer = QTimer(self)
        self.watchdog_timer.setInterval(10000) # Check every 10 seconds
        self.watchdog_timer.timeout.connect(self.check_ai_status)
        self.watchdog_timer.start()

    def check_ai_status(self):
        worker = BaseWorker(self._async_check)
        worker.signals.result.connect(self._on_check_result)
        self.thread_pool.start(worker)

    def _async_check(self):
        # start_silently already checks if it is running first, and only starts if not.
        return asyncio.run(self.ollama.start_silently())

    def _on_check_result(self, result):
        success, message = result
        if success:
            self.status_label.setText("🟢 AI Engine Online (Ollama)")
            self.status_label.setStyleSheet("margin-top: 20px; font-weight: bold; color: #22C55E;")
            # Now check the model
            self.check_model_status()
        else:
            self.status_label.setText(f"🔴 AI Engine Error: {message}")
            self.status_label.setStyleSheet("margin-top: 20px; font-weight: bold; color: #EF4444;")
            self.model_label.setText("Cannot check model: AI engine offline.")

    def check_model_status(self):
        worker = BaseWorker(self._async_check_model)
        worker.signals.result.connect(self._on_model_check_result)
        self.thread_pool.start(worker)

    def _async_check_model(self):
        return asyncio.run(self.model_mgr.has_required_model())

    def _on_model_check_result(self, has_model: bool):
        if has_model:
            self.model_label.setText(f"🟢 Model Ready: {self.model_mgr.target_model}")
            self.model_label.setStyleSheet("font-weight: bold; color: #22C55E;")
            self.btn_download_model.hide()
            self.download_progress.hide()
        else:
            self.model_label.setText(f"🔴 Missing required model: {self.model_mgr.target_model}")
            self.model_label.setStyleSheet("font-weight: bold; color: #EF4444;")
            self.btn_download_model.show()

    def start_model_download(self):
        self.btn_download_model.setEnabled(False)
        self.btn_download_model.setText("Downloading...")
        self.download_progress.show()
        self.download_progress.setValue(0)
        
        self.download_signals = DownloadSignals()
        self.download_signals.progress.connect(self._on_download_progress)
        self.download_signals.finished.connect(self._on_download_finished)
        
        worker = DownloadWorker(self._async_download_model, self.download_signals)
        self.thread_pool.start(worker)

    async def _async_download_model(self, signals):
        try:
            async for status in self.model_mgr.pull_model_stream():
                signals.progress.emit(status)
            
            # Smoke test after pull
            is_ready = await self.model_mgr.smoke_test()
            signals.finished.emit(is_ready, "Download complete")
        except Exception as e:
            signals.finished.emit(False, str(e))

    def _on_download_progress(self, status: dict):
        if "error" in status:
            self.model_label.setText(f"Download Error: {status['error']}")
            return
            
        text = status.get("status", "Downloading...")
        
        if "completed" in status and "total" in status:
            completed = status["completed"]
            total = status["total"]
            if total > 0:
                percent = int((completed / total) * 100)
                self.download_progress.setValue(percent)
                text = f"{text} ({percent}%)"
        
        self.model_label.setText(text)

    def _on_download_finished(self, success: bool, message: str):
        if success:
            self.check_model_status()
        else:
            self.btn_download_model.setEnabled(True)
            self.btn_download_model.setText("Retry Download")
            self.model_label.setText(f"Error: {message}")
            self.model_label.setStyleSheet("font-weight: bold; color: #EF4444;")
