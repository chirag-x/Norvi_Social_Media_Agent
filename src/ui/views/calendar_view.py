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
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Content Calendar")
        title.setProperty("class", "title")
        header_layout.addWidget(title)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setProperty("class", "secondary")
        refresh_btn.clicked.connect(self.load_schedule)
        header_layout.addWidget(refresh_btn)
        
        self.btn_clear = QPushButton("Clear Uploaded")
        self.btn_clear.setProperty("class", "secondary")
        self.btn_clear.clicked.connect(self.clear_uploaded)
        header_layout.addWidget(self.btn_clear)
        
        self.btn_remove = QPushButton("Remove Selected")
        self.btn_remove.setStyleSheet("background-color: #EF4444; color: white; border-radius: 4px; padding: 6px 15px; font-weight: bold;")
        self.btn_remove.clicked.connect(self.remove_selected)
        header_layout.addWidget(self.btn_remove)
        
        main_layout.addLayout(header_layout)
        
        # Table
        from PySide6.QtWidgets import QAbstractItemView
        self.table = QTableWidget(0, 4)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setHorizontalHeaderLabels(["DATE / TIME", "VIDEO TITLE", "PLATFORMS", "STATUS"])
        
        # Column resize policy:
        # Date, Platforms, Status → fixed minimum with Interactive resizing
        # Title → takes all remaining space (Stretch)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Interactive)
        header.setStretchLastSection(False)
        header.setMinimumSectionSize(80)
        
        # Align header text to center for all columns
        for col in range(4):
            item = self.table.horizontalHeaderItem(col)
            if item:
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Default column widths
        self.table.setColumnWidth(0, 185)   # Date / Time
        self.table.setColumnWidth(2, 160)   # Platforms
        self.table.setColumnWidth(3, 160)   # Status
        
        self.table.setStyleSheet("QTableWidget { gridline-color: transparent; }")
        self.table.setAlternatingRowColors(False)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(60)
        
        main_layout.addWidget(self.table)


    def load_schedule(self):
        self.table.setRowCount(0)
        try:
            with self.db.get_connection() as conn:
                cursor = conn.execute("SELECT * FROM scheduled_posts ORDER BY schedule_time ASC")
                posts = cursor.fetchall()
                
                for i, post in enumerate(posts):
                    self.table.insertRow(i)
                    
                    from PySide6.QtGui import QColor
                    C = Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter

                    # Store ID in the first column's user role
                    date_item = QTableWidgetItem(post["schedule_time"])
                    date_item.setData(Qt.ItemDataRole.UserRole, post["id"])
                    date_item.setTextAlignment(C)
                    
                    title_item = QTableWidgetItem(post["title"] or "")
                    title_item.setTextAlignment(C)
                    
                    platform_item = QTableWidgetItem(post["platforms"])
                    platform_item.setTextAlignment(C)

                    status_item = QTableWidgetItem(post["status"])
                    status_item.setTextAlignment(C)
                    if post["status"] == "PENDING":
                        status_item.setForeground(QColor("#EAB308"))
                    elif post["status"] == "PUBLISHED":
                        status_item.setForeground(QColor("#22C55E"))
                    elif post["status"] == "NATIVE_SCHEDULED":
                        status_item.setForeground(QColor("#3B82F6"))
                    elif post["status"] == "FAILED":
                        status_item.setForeground(QColor("#EF4444"))
                    elif post["status"] == "PUBLISHING...":
                        status_item.setForeground(QColor("#A855F7"))

                    self.table.setItem(i, 0, date_item)
                    self.table.setItem(i, 1, title_item)
                    self.table.setItem(i, 2, platform_item)
                    self.table.setItem(i, 3, status_item)
        except Exception:
            pass

    def remove_selected(self):
        row = self.table.currentRow()
        if row < 0:
            return
            
        item = self.table.item(row, 0)
        if not item:
            return
            
        post_id = item.data(Qt.ItemDataRole.UserRole)
        
        try:
            with self.db.get_connection() as conn:
                conn.execute("DELETE FROM scheduled_posts WHERE id = ?", (post_id,))
                conn.commit()
            
            self.load_schedule()
        except Exception:
            pass

    def clear_uploaded(self):
        from PySide6.QtWidgets import QMessageBox
        msg = QMessageBox(self)
        msg.setWindowTitle("Clear Uploaded")
        msg.setText("Are you sure you want to clear all successfully published and scheduled logs? Pending/uploading videos will be kept.")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.No)
        msg.setStyleSheet("QMessageBox { background-color: #F8FAFC; } QLabel { color: #0F172A; font-size: 14px; } QPushButton { background-color: #3B82F6; color: white; border-radius: 4px; padding: 6px 15px; font-weight: bold; min-width: 60px; } QPushButton:hover { background-color: #2563EB; }")
        
        reply = msg.exec()
        if reply == QMessageBox.StandardButton.Yes:
            try:
                with self.db.get_connection() as conn:
                    conn.execute("DELETE FROM scheduled_posts WHERE status IN ('PUBLISHED', 'NATIVE_SCHEDULED')")
                    conn.commit()
                self.load_schedule()
            except Exception:
                pass

