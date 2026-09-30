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
        
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        
        from PySide6.QtWidgets import QScrollArea
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        main_layout = QVBoxLayout(scroll_content)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        scroll.setWidget(scroll_content)
        outer_layout.addWidget(scroll)
        
        title = QLabel("Dashboard")
        title.setProperty("class", "title")
        main_layout.addWidget(title)
        
        # Hero Card
        from PySide6.QtWidgets import QFrame
        hero_card = QFrame()
        hero_card.setObjectName("card")
        hero_layout = QVBoxLayout(hero_card)
        
        hero_title = QLabel("Welcome to Norvi Agent! 🚀")
        hero_title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        hero_layout.addWidget(hero_title)
        
        hero_desc = QLabel("Your autonomous pipeline for discovering, creating, and publishing viral content across all platforms. Select an option from the sidebar to begin building your empire.")
        hero_desc.setProperty("class", "subtitle")
        hero_desc.setWordWrap(True)
        hero_layout.addWidget(hero_desc)
        
        main_layout.addWidget(hero_card)
        
        # Status Card
        status_card = QFrame()
        status_card.setObjectName("card")
        status_layout = QVBoxLayout(status_card)
        
        status_title = QLabel("System Status")
        status_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        status_layout.addWidget(status_title)
        
        # Brain Status
        self.brain_label = QLabel("🧠 Brain loading...")
        self.brain_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #EAB308; margin-top: 10px;")
        status_layout.addWidget(self.brain_label)
        
        self.btn_download_model = QPushButton("Download Required AI Model")
        self.btn_download_model.setProperty("class", "primary")
        self.btn_download_model.setFixedWidth(300)
        self.btn_download_model.hide()
        self.btn_download_model.clicked.connect(self.start_model_download)
        status_layout.addWidget(self.btn_download_model)
        
        from PySide6.QtWidgets import QProgressBar
        self.download_progress = QProgressBar()
        self.download_progress.setFixedWidth(400)
        self.download_progress.hide()
        status_layout.addWidget(self.download_progress)
        
        # Active Source Box
        self.active_source_label = QLabel("🎬 No active content source selected.")
        self.active_source_label.setProperty("class", "subtitle")
        status_layout.addWidget(self.active_source_label)
        
        # Quick Stats Row
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)
        
        # Stat 1
        stat1 = QFrame()
        stat1.setObjectName("card")
        stat1_layout = QVBoxLayout(stat1)
        stat1_title = QLabel("AI Pipeline")
        stat1_title.setProperty("class", "subtitle")
        self.stat_ai = QLabel("Initializing...")
        self.stat_ai.setStyleSheet("color: #EAB308; font-size: 24px; font-weight: bold;")
        stat1_layout.addWidget(stat1_title)
        stat1_layout.addWidget(self.stat_ai)
        stats_layout.addWidget(stat1)
        
        # Stat 2
        stat2 = QFrame()
        stat2.setObjectName("card")
        stat2_layout = QVBoxLayout(stat2)
        stat2_title = QLabel("Platforms Connected")
        stat2_title.setProperty("class", "subtitle")
        self.stat_platforms = QLabel("0")
        self.stat_platforms.setStyleSheet("color: #38BDF8; font-size: 24px; font-weight: bold;")
        stat2_layout.addWidget(stat2_title)
        stat2_layout.addWidget(self.stat_platforms)
        stats_layout.addWidget(stat2)
        
        main_layout.addLayout(stats_layout)
        
        main_layout.addWidget(status_card)
        
        from src.app.state import AppState
        AppState.get_instance().active_source_changed.connect(self._on_active_source_changed)
        
        main_layout.addStretch()
        
        # Initial check
        self.check_ai_status()
        self.update_platform_count()
        
    def update_platform_count(self):
        """
        Count only platforms that are truly authenticated:
        - OAuth platforms (YouTube, TikTok): must have a refresh_token saved after completing the OAuth flow
        - Token platforms (Instagram, Facebook, X): must have an access_token entered by the user
        Simply having a client_id/secret saved does NOT count as connected.
        """
        try:
            from src.storage.database.database import DatabaseManager
            db = DatabaseManager.get_instance()
            with db.get_connection() as conn:
                cursor = conn.execute(
                    """SELECT COUNT(*) as cnt FROM api_keys 
                       WHERE (refresh_token IS NOT NULL AND refresh_token != '')
                          OR (access_token IS NOT NULL AND access_token != '')"""
                )
                row = cursor.fetchone()
                count = row["cnt"] if row else 0
        except Exception:
            count = 0
        self.stat_platforms.setText(str(count))
        
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
        self.brain_label.setText("🧠 Brain loading...")
        self.brain_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #EAB308; margin-top: 10px;")
        worker = BaseWorker(self._async_check)
        worker.signals.result.connect(self._on_check_result)
        self.thread_pool.start(worker)

    def _async_check(self):
        # start_silently already checks if it is running first, and only starts if not.
        return asyncio.run(self.ollama.start_silently())

    def _on_check_result(self, result):
        success, message = result
        if success:
            # Ollama is online, now check the model
            self.check_model_status()
        else:
            self.brain_label.setText("🧠 Brain Offline")
            self.brain_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #EF4444; margin-top: 10px;")
            self.stat_ai.setText("Offline")
            self.stat_ai.setStyleSheet("color: #EF4444; font-size: 24px; font-weight: bold;")

    def check_model_status(self):
        worker = BaseWorker(self._async_check_model)
        worker.signals.result.connect(self._on_model_check_result)
        self.thread_pool.start(worker)

    def _async_check_model(self):
        return asyncio.run(self.model_mgr.has_required_model())

    def _on_model_check_result(self, has_model: bool):
        if has_model:
            self.brain_label.setText("🧠 Brain connected, ready")
            self.brain_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #22C55E; margin-top: 10px;")
            self.stat_ai.setText("Active")
            self.stat_ai.setStyleSheet("color: #22C55E; font-size: 24px; font-weight: bold;")
            self.btn_download_model.hide()
            self.download_progress.hide()
        else:
            self.brain_label.setText("🧠 Brain Missing Knowledge")
            self.brain_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #EF4444; margin-top: 10px;")
            self.stat_ai.setText("Needs Model")
            self.stat_ai.setStyleSheet("color: #EAB308; font-size: 24px; font-weight: bold;")
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
