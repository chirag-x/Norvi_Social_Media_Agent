from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout
)
from PySide6.QtCore import Qt
from src.storage.database.database import DatabaseManager

class AnalyticsView(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager.get_instance()
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Header
        title = QLabel("Performance Analytics")
        title.setProperty("class", "title")
        main_layout.addWidget(title)
        
        subtitle = QLabel("Aggregate metrics across all connected platforms (Phase 24)")
        subtitle.setStyleSheet("color: #94A3B8; margin-bottom: 20px;")
        main_layout.addWidget(subtitle)
        
        # Internal Metrics Grid (App usage)
        self.internal_grid = QGridLayout()
        self.lbl_total_extracted = self._create_stat_card("Total Clips Extracted", "0", "clips", self.internal_grid, 0, 0)
        self.lbl_total_scheduled = self._create_stat_card("Videos Scheduled", "0", "queue", self.internal_grid, 0, 1)
        self.lbl_total_published = self._create_stat_card("Videos Published", "0", "live", self.internal_grid, 0, 2)
        main_layout.addLayout(self.internal_grid)
        
        # Platform Metrics Grid (Simulated for now until Phase 19 is fully connected)
        platform_title = QLabel("\nPlatform Reach (Simulated)")
        platform_title.setStyleSheet("font-size: 18px; font-weight: bold; color: white; margin-top: 20px;")
        main_layout.addWidget(platform_title)
        
        self.platform_grid = QGridLayout()
        self._create_stat_card("Total Views", "14.2K", "YouTube Shorts", self.platform_grid, 0, 0)
        self._create_stat_card("Total Likes", "1.2K", "YouTube Shorts", self.platform_grid, 0, 1)
        self._create_stat_card("Total Views", "89.5K", "TikTok", self.platform_grid, 1, 0)
        self._create_stat_card("Total Likes", "12.4K", "TikTok", self.platform_grid, 1, 1)
        self._create_stat_card("Total Views", "3.4K", "Instagram Reels", self.platform_grid, 2, 0)
        self._create_stat_card("Total Likes", "250", "Instagram Reels", self.platform_grid, 2, 1)
        
        main_layout.addLayout(self.platform_grid)
        main_layout.addStretch()

    def _create_stat_card(self, title: str, value: str, subtitle: str, grid: QGridLayout, row: int, col: int) -> QLabel:
        card = QFrame()
        card.setStyleSheet("background-color: #1E293B; border-radius: 8px; padding: 20px; border: 1px solid #374151;")
        layout = QVBoxLayout(card)
        
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #94A3B8; font-weight: bold; font-size: 14px; border: none;")
        layout.addWidget(lbl_title)
        
        lbl_val = QLabel(value)
        lbl_val.setStyleSheet("color: white; font-weight: bold; font-size: 28px; border: none;")
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
