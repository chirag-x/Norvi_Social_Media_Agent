from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout, QPushButton
)
from PySide6.QtCore import Qt, QThreadPool
from src.storage.database.database import DatabaseManager
from src.services.analytics.analytics_engine import AnalyticsEngine
from src.workers.base import BaseWorker
class AnalyticsView(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager.get_instance()
        self.threadpool = QThreadPool()
        self.analytics_engine = AnalyticsEngine()
        self.setup_ui()
        self.load_data()

    def showEvent(self, event):
        super().showEvent(event)
        self.load_data()

    def setup_ui(self):
        from PySide6.QtWidgets import QScrollArea
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { background: transparent; } QWidget#scroll_widget { background: transparent; }")
        scroll_widget = QWidget()
        scroll_widget.setObjectName("scroll_widget")
        main_layout = QVBoxLayout(scroll_widget)
        layout_outer = QVBoxLayout(self)
        layout_outer.setContentsMargins(0, 0, 0, 0)
        layout_outer.addWidget(scroll)
        scroll.setWidget(scroll_widget)
        
        # Header
        title = QLabel("Performance Analytics")
        title.setProperty("class", "title")
        main_layout.addWidget(title)
        
        subtitle = QLabel("Aggregate metrics across all connected platforms (Phase 24)")
        subtitle.setStyleSheet(" margin-bottom: 20px;")
        main_layout.addWidget(subtitle)
        
        # Internal Metrics Grid (App usage)
        self.internal_grid = QGridLayout()
        self.lbl_total_extracted = self._create_stat_card("Total Clips Extracted", "0", "clips", self.internal_grid, 0, 0)
        self.lbl_total_scheduled = self._create_stat_card("Videos Scheduled", "0", "queue", self.internal_grid, 0, 1)
        self.lbl_total_published = self._create_stat_card("Videos Published", "0", "live", self.internal_grid, 0, 2)
        main_layout.addLayout(self.internal_grid)
        
        # Platform Metrics Grid
        platform_header = QHBoxLayout()
        platform_title = QLabel("\nPlatform Reach")
        platform_title.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 20px;")
        
        self.btn_refresh = QPushButton("Refresh Analytics from Network")
        self.btn_refresh.setProperty("class", "primary")
        self.btn_refresh.clicked.connect(self.refresh_analytics)
        
        self.lbl_status = QLabel("")
        self.lbl_status.setStyleSheet("color: #64748B; margin-top: 20px;")
        
        platform_header.addWidget(platform_title)
        platform_header.addStretch()
        platform_header.addWidget(self.lbl_status)
        platform_header.addWidget(self.btn_refresh)
        platform_header.setAlignment(Qt.AlignBottom)
        
        main_layout.addLayout(platform_header)
        
        self.platform_grid = QGridLayout()
        self.lbl_yt_views = self._create_stat_card("Total Views", "0", "YouTube Shorts", self.platform_grid, 0, 0)
        self.lbl_yt_likes = self._create_stat_card("Total Likes", "0", "YouTube Shorts", self.platform_grid, 0, 1)
        self.lbl_tiktok_views = self._create_stat_card("Total Views", "0", "TikTok", self.platform_grid, 1, 0)
        self.lbl_tiktok_likes = self._create_stat_card("Total Likes", "0", "TikTok", self.platform_grid, 1, 1)
        self.lbl_ig_views = self._create_stat_card("Total Views", "0", "Instagram Reels", self.platform_grid, 2, 0)
        self.lbl_ig_likes = self._create_stat_card("Total Likes", "0", "Instagram Reels", self.platform_grid, 2, 1)
        self.lbl_fb_views = self._create_stat_card("Total Views", "0", "Facebook Reels", self.platform_grid, 3, 0)
        self.lbl_fb_likes = self._create_stat_card("Total Likes", "0", "Facebook Reels", self.platform_grid, 3, 1)
        self.lbl_tw_views = self._create_stat_card("Total Views", "0", "X (Twitter)", self.platform_grid, 4, 0)
        self.lbl_tw_likes = self._create_stat_card("Total Likes", "0", "X (Twitter)", self.platform_grid, 4, 1)
        
        main_layout.addLayout(self.platform_grid)
        main_layout.addStretch()

    def _create_stat_card(self, title: str, value: str, subtitle: str, grid: QGridLayout, row: int, col: int) -> QLabel:
        card = QFrame()
        card.setObjectName("card")
        card.setMinimumHeight(130)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet(" font-weight: bold; font-size: 14px; border: none;")
        layout.addWidget(lbl_title)
        
        lbl_val = QLabel(value)
        lbl_val.setStyleSheet(" font-weight: bold; font-size: 28px; border: none;")
        layout.addWidget(lbl_val)
        
        lbl_sub = QLabel(subtitle)
        lbl_sub.setStyleSheet("color: #64748B; font-size: 12px; border: none;")
        layout.addWidget(lbl_sub)
        
        grid.addWidget(card, row, col)
        return lbl_val

    def load_data(self):
        try:
            with self.db.get_connection() as conn:
                # Clips Extracted
                cursor = conn.execute("SELECT COUNT(*) FROM extracted_clips")
                total_extracted = cursor.fetchone()[0]
                self.lbl_total_extracted.setText(str(total_extracted))
                
                # Scheduled vs Published
                cursor = conn.execute("SELECT status, COUNT(*) FROM scheduled_posts GROUP BY status")
                counts = cursor.fetchall()
                
                scheduled = 0
                published = 0
                for row in counts:
                    if row[0] == "PENDING":
                        scheduled = row[1]
                    elif row[0] == "PUBLISHED":
                        published = row[1]
                        
                self.lbl_total_scheduled.setText(str(scheduled))
                self.lbl_total_published.setText(str(published))
        except Exception as e:
            print(f"Failed to load analytics: {e}")
    def refresh_analytics(self):
        self.btn_refresh.setEnabled(False)
        self.lbl_status.setText("Fetching network stats...")
        
        worker = BaseWorker(self.analytics_engine.fetch_all_stats)
        worker.signals.result.connect(self.on_analytics_result)
        worker.signals.error.connect(self.on_analytics_error)
        worker.signals.finished.connect(self.on_analytics_finished)
        self.threadpool.start(worker)

    def on_analytics_result(self, stats: dict):
        def format_number(num):
            if num >= 1000000:
                return f"{num/1000000:.1f}M"
            elif num >= 1000:
                return f"{num/1000:.1f}K"
            return str(num)

        yt = stats.get('youtube', {})
        self.lbl_yt_views.setText(format_number(yt.get('views', 0)))
        self.lbl_yt_likes.setText(format_number(yt.get('likes', 0)))
        
        tiktok = stats.get('tiktok', {})
        self.lbl_tiktok_views.setText(format_number(tiktok.get('views', 0)))
        self.lbl_tiktok_likes.setText(format_number(tiktok.get('likes', 0)))
        
        ig = stats.get('instagram', {})
        self.lbl_ig_views.setText(format_number(ig.get('views', 0)))
        self.lbl_ig_likes.setText(format_number(ig.get('likes', 0)))

        fb = stats.get('facebook', {})
        self.lbl_fb_views.setText(format_number(fb.get('views', 0)))
        self.lbl_fb_likes.setText(format_number(fb.get('likes', 0)))

        tw = stats.get('twitter', {})
        self.lbl_tw_views.setText(format_number(tw.get('views', 0)))
        self.lbl_tw_likes.setText(format_number(tw.get('likes', 0)))

        self.lbl_status.setText("Updated just now.")

    def on_analytics_error(self, err_tuple):
        print(f"Analytics refresh error: {err_tuple}")
        self.lbl_status.setText("Failed to update.")

    def on_analytics_finished(self):
        self.btn_refresh.setEnabled(True)
