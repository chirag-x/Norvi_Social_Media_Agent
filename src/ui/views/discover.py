from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QListWidget, QListWidgetItem, QComboBox, QScrollArea, QFrame
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QDesktopServices
from PySide6.QtCore import QUrl
import asyncio

from src.workers.base import BaseWorker
from PySide6.QtCore import QThreadPool
from src.discovery.youtube import YouTubeProvider
from src.discovery.provider import VideoResult

class VideoItemWidget(QFrame):
    def __init__(self, video: VideoResult):
        super().__init__()
        self.video = video
        self.setProperty("class", "video_item")
        self.setStyleSheet("QFrame { background-color: transparent; padding: 15px 10px; margin-bottom: 5px; }")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        # Thumbnail
        self.thumb_label = QLabel()
        self.thumb_label.setFixedSize(160, 90)
        self.thumb_label.setStyleSheet("border-radius: 8px;")
        self.thumb_label.setScaledContents(True)
        layout.addWidget(self.thumb_label)
        
        # Details
        details_layout = QVBoxLayout()
        details_layout.setSpacing(5)
        
        title = QLabel(video.title)
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        title.setWordWrap(True)
        details_layout.addWidget(title)
        
        views_formatted = f"{video.views:,}" if isinstance(video.views, int) else video.views
        meta = QLabel(f"{video.channel}  •  {views_formatted} views  •  Duration: {video.duration}")
        meta.setProperty("class", "subtitle")
        details_layout.addWidget(meta)
        
        btn_layout = QHBoxLayout()
        open_btn = QPushButton("Watch on YouTube")
        open_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        open_btn.setStyleSheet("background-color: #EF4444; color: white; border-radius: 4px; padding: 6px 15px; font-weight: bold;")
        open_btn.clicked.connect(self._open_url)
        btn_layout.addWidget(open_btn)
        
        select_btn = QPushButton("Select Source")
        select_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        select_btn.setStyleSheet("background-color: #3B82F6; color: white; border-radius: 4px; padding: 6px 15px; font-weight: bold;")
        select_btn.clicked.connect(self._select_source)
        btn_layout.addWidget(select_btn)
        btn_layout.addStretch()
        
        details_layout.addLayout(btn_layout)
        layout.addLayout(details_layout)
        layout.setStretch(1, 1)
        
        # Start async thumbnail load
        if self.video.thumbnail:
            self._load_thumbnail()

    def _load_thumbnail(self):
        worker = BaseWorker(self._sync_fetch_thumb)
        worker.signals.result.connect(self._on_thumb_loaded)
        QThreadPool.globalInstance().start(worker)

    def _sync_fetch_thumb(self):
        import urllib.request
        try:
            req = urllib.request.Request(self.video.thumbnail, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.read()
        except Exception as e:
            return None

    def _on_thumb_loaded(self, data):
        if data:
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            self.thumb_label.setPixmap(pixmap)

    def _open_url(self):
        QDesktopServices.openUrl(QUrl(self.video.url))

    def _select_source(self):
        from src.app.state import AppState
        AppState.get_instance().active_source = self.video
        from PySide6.QtWidgets import QApplication
        from src.ui.main_window import MainWindow
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, MainWindow):
                widget.navigate_to("clip_lab")
                break


class DiscoverView(QWidget):
    def __init__(self):
        super().__init__()
        self.thread_pool = QThreadPool.globalInstance()
        self.youtube = YouTubeProvider()
        
        main_layout = QVBoxLayout(self)
        
        # Header
        title = QLabel("Content Discovery")
        title.setProperty("class", "title")
        main_layout.addWidget(title)
        
        # Search Bar
        search_layout = QHBoxLayout()
        # Remove AlignVCenter because it can squash things if heights are mismatched
        # Just use minimum heights to give everything breathing room
        
        self.niche_combo = QComboBox()
        self.niche_combo.addItems(["General", "Tech", "Gaming", "Finance", "Lifestyle", "Education"])
        self.niche_combo.setFixedWidth(150)
        self.niche_combo.setMinimumHeight(40)
        search_layout.addWidget(self.niche_combo)
        
        self.country_combo = QComboBox()
        self.country_combo.addItems(["Global", "United States", "India", "United Kingdom", "Canada", "Australia"])
        self.country_combo.setFixedWidth(130)
        self.country_combo.setMinimumHeight(40)
        search_layout.addWidget(self.country_combo)
        
        self.duration_combo = QComboBox()
        self.duration_combo.addItems(["Any Length", "0 - 3 mins", "3 - 10 mins", "10 - 20 mins", "20+ mins"])
        self.duration_combo.setFixedWidth(120)
        self.duration_combo.setMinimumHeight(40)
        search_layout.addWidget(self.duration_combo)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search topics, keywords, or paste a YouTube URL...")
        self.search_input.setMinimumHeight(40)
        self.search_input.returnPressed.connect(self.perform_search)
        search_layout.addWidget(self.search_input)
        
        self.search_btn = QPushButton("Search")
        self.search_btn.setProperty("class", "primary")
        self.search_btn.setMinimumHeight(40)
        self.search_btn.clicked.connect(self.perform_search)
        search_layout.addWidget(self.search_btn)
        
        main_layout.addLayout(search_layout)
        
        # Status Label
        self.status_label = QLabel("")
        self.status_label.setProperty("class", "subtitle")
        self.status_label.hide()
        main_layout.addWidget(self.status_label)
        
        # Results List
        self.results_list = QListWidget()
        self.results_list.setStyleSheet("QListWidget { background-color: transparent; border: none; } QListWidget::item { background-color: transparent; }")
        main_layout.addWidget(self.results_list)

    def perform_search(self):
        query = self.search_input.text().strip()
        niche = self.niche_combo.currentText()
        
        is_url = query.startswith("http://") or query.startswith("https://")
        
        if not is_url:
            if not query:
                if niche == "General":
                    query = "viral trending"
                else:
                    query = f"top trending {niche.lower()}"
                
            country = self.country_combo.currentText()
            if country != "Global":
                query = f"{query} in {country}"
                
            duration_filter = self.duration_combo.currentText()
            if duration_filter == "0 - 3 mins":
                query = f"{query} #shorts"
            
        self.results_list.clear()
        self.search_btn.setEnabled(False)
        self.status_label.setText("Searching YouTube...")
        self.status_label.show()
        
        duration_filter = self.duration_combo.currentText()
        
        worker = BaseWorker(self._async_search, query, niche, duration_filter)
        worker.signals.result.connect(self._on_search_results)
        worker.signals.error.connect(self._on_search_error)
        self.thread_pool.start(worker)

    def _async_search(self, query: str, niche: str, duration_filter: str) -> list:
        # If the user pasted a direct YouTube link, bypass the complex discovery algorithm
        if query.startswith("http://") or query.startswith("https://"):
            import asyncio
            return asyncio.run(self.youtube.get_by_url(query))
            
        # Fetch 200 results to cast a massive net before strictly filtering down to the Top 5
        import asyncio
        return asyncio.run(self.youtube.search(query, niche, duration_filter=duration_filter, max_results=200))

    def _on_search_results(self, videos: list):
        self.search_btn.setEnabled(True)
        if not videos:
            self.status_label.setText("No results found.")
            return
            
        self.status_label.hide()
        
        for video in videos:
            item = QListWidgetItem(self.results_list)
            widget = VideoItemWidget(video)
            
            # Need to set size hint so it displays correctly
            item.setSizeHint(QSize(0, 190))
            self.results_list.addItem(item)
            self.results_list.setItemWidget(item, widget)

    def _on_search_error(self, err):
        self.search_btn.setEnabled(True)
        self.status_label.setText(f"Error during search: {err[1]}")
