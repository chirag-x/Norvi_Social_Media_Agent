from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QDateTimeEdit
)
from PySide6.QtCore import Qt, QDateTime
from src.storage.database.database import DatabaseManager

class CalendarView(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager.get_instance()
        self.setup_ui()
        self.load_schedule()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Content Calendar")
        title.setProperty("class", "title")
        header_layout.addWidget(title)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setProperty("class", "btn-secondary")
        refresh_btn.clicked.connect(self.load_schedule)
        header_layout.addWidget(refresh_btn)
        
        main_layout.addLayout(header_layout)
        
        # Table
        from PySide6.QtWidgets import QAbstractItemView
        self.table = QTableWidget(0, 4)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setHorizontalHeaderLabels(["Date / Time", "Video Title", "Platforms", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet("QTableWidget { background-color: #1F2937; border: 1px solid #374151; border-radius: 8px; } QHeaderView::section { background-color: #111827; }")
        
        main_layout.addWidget(self.table)

    def load_schedule(self):
        self.table.setRowCount(0)
        try:
            with self.db.get_connection() as conn:
                cursor = conn.execute("SELECT * FROM scheduled_posts ORDER BY schedule_time ASC")
                posts = cursor.fetchall()
                
                for i, post in enumerate(posts):
                    self.table.insertRow(i)
                    self.table.setItem(i, 0, QTableWidgetItem(post["schedule_time"]))
                    self.table.setItem(i, 1, QTableWidgetItem(post["title"]))
                    self.table.setItem(i, 2, QTableWidgetItem(post["platforms"]))
                    
                    status_item = QTableWidgetItem(post["status"])
                    if post["status"] == "PENDING":
                        status_item.setForeground(Qt.GlobalColor.yellow)
                    elif post["status"] == "PUBLISHED":
                        status_item.setForeground(Qt.GlobalColor.green)
                        
                    self.table.setItem(i, 3, status_item)
        except Exception:
            pass
