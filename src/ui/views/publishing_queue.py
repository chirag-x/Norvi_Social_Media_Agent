import os
import json
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QListWidget, QPushButton, QTextEdit, QLineEdit, QSplitter
)
from PySide6.QtCore import Qt
from src.workers.base import BaseWorker
from PySide6.QtCore import QThreadPool

class PublishingQueueView(QWidget):
    def __init__(self):
        super().__init__()
        self.outputs_dir = Path("outputs")
        self.setup_ui()
        self.refresh_queue()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Publishing Queue")
        title.setProperty("class", "title")
        header_layout.addWidget(title)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setProperty("class", "btn-secondary")
        refresh_btn.clicked.connect(self.refresh_queue)
        header_layout.addWidget(refresh_btn)
        
        main_layout.addLayout(header_layout)
        
        # Splitter for layout
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left Panel (List of Videos)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        self.video_list = QListWidget()
        self.video_list.currentItemChanged.connect(self.on_video_selected)
        left_layout.addWidget(self.video_list)
        
        splitter.addWidget(left_panel)
        
        # Right Panel (Metadata Editor)
        self.right_panel = QWidget()
        right_layout = QVBoxLayout(self.right_panel)
        right_layout.setContentsMargins(10, 0, 0, 0)
        
        self.lbl_selected = QLabel("Select a video to prepare for publishing.")
        self.lbl_selected.setStyleSheet("color: #9CA3AF; font-weight: bold;")
        right_layout.addWidget(self.lbl_selected)
        
        right_layout.addWidget(QLabel("Post Title:"))
        self.txt_title = QLineEdit()
        right_layout.addWidget(self.txt_title)
        
        right_layout.addWidget(QLabel("Description & Hashtags:"))
        self.txt_desc = QTextEdit()
        right_layout.addWidget(self.txt_desc)
        
        # Schedule Time Picker
        time_layout = QHBoxLayout()
        time_layout.addWidget(QLabel("Publish Date/Time:"))
        from PySide6.QtWidgets import QDateTimeEdit
        from PySide6.QtCore import QDateTime
        self.dt_picker = QDateTimeEdit(QDateTime.currentDateTime())
        self.dt_picker.setCalendarPopup(True)
        time_layout.addWidget(self.dt_picker)
        right_layout.addLayout(time_layout)
        
        # Action Buttons
        btn_layout = QHBoxLayout()
        self.btn_ai = QPushButton("Generate Metadata (AI)")
        self.btn_ai.setProperty("class", "btn-primary")
        self.btn_ai.clicked.connect(self.generate_metadata)
        btn_layout.addWidget(self.btn_ai)
        
        self.btn_schedule = QPushButton("Schedule Upload")
        self.btn_schedule.setProperty("class", "btn-secondary")
        self.btn_schedule.clicked.connect(self.schedule_upload)
        btn_layout.addWidget(self.btn_schedule)
        
        right_layout.addLayout(btn_layout)
        self.right_panel.hide() # Hide until selected
        
        splitter.addWidget(self.right_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        main_layout.addWidget(splitter)
        
        # Status
        self.status_label = QLabel("")
        main_layout.addWidget(self.status_label)

    def refresh_queue(self):
        self.video_list.clear()
        if not self.outputs_dir.exists():
            return
            
        for file in self.outputs_dir.glob("*.mp4"):
            self.video_list.addItem(file.name)
            
    def on_video_selected(self, current, previous):
        if not current:
            self.right_panel.hide()
            return
            
        filename = current.text()
        self.lbl_selected.setText(f"Preparing: {filename}")
        self.txt_title.clear()
        self.txt_desc.clear()
        self.status_label.clear()
        
        # Load existing JSON if we saved one
        json_file = self.outputs_dir / f"{Path(filename).stem}.json"
        if json_file.exists():
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.txt_title.setText(data.get('title', ''))
                    self.txt_desc.setText(data.get('description', ''))
            except Exception:
                pass
                
        self.right_panel.show()

    def generate_metadata(self):
        item = self.video_list.currentItem()
        if not item:
            return
            
        filename = item.text()
        clean_title = Path(filename).stem
        
        self.btn_ai.setEnabled(False)
        self.status_label.setText("Asking Gemma AI to write a viral description...")
        
        worker = BaseWorker(self._async_generate, clean_title)
        worker.signals.result.connect(self._on_generate_success)
        worker.signals.error.connect(self._on_generate_error)
        QThreadPool.globalInstance().start(worker)
        
    def _async_generate(self, video_title: str):
        import asyncio
        from src.services.ai.gemma_engine import GemmaEngine
        engine = GemmaEngine()
        
        prompt = f"""
        You are a TikTok/Shorts viral marketing expert. 
        I have a short video clip named: "{video_title}"
        
        Write a viral post description for this video.
        It must include:
        1. A strong hook sentence. If the title contains "(Part 1)", tease that there is more coming. If the title contains "(Part 2)", remind them to watch Part 1.
        2. 1-2 short engaging sentences.
        3. 5-7 highly relevant hashtags.
        
        DO NOT wrap in json. Just output the raw text.
        """
        
        return asyncio.run(engine.generate_text(prompt))
        
    def _on_generate_success(self, text: str):
        self.btn_ai.setEnabled(True)
        self.txt_title.setText(self.video_list.currentItem().text().replace('.mp4', ''))
        self.txt_desc.setText(text)
        self.status_label.setText("Metadata generated! You can edit it manually before scheduling.")
        self.status_label.setStyleSheet("color: #22C55E;")
        
        # Save to JSON
        filename = self.video_list.currentItem().text()
        json_file = self.outputs_dir / f"{Path(filename).stem}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                "title": self.txt_title.text(),
                "description": text
            }, f)
            
    def _on_generate_error(self, err):
        self.btn_ai.setEnabled(True)
        self.status_label.setText(f"Error: {err[1]}")
        self.status_label.setStyleSheet("color: #EF4444;")
        
    def schedule_upload(self):
        item = self.video_list.currentItem()
        if not item:
            return
            
        filename = item.text()
        video_path = str((self.outputs_dir / filename).absolute())
        title = self.txt_title.text()
        desc = self.txt_desc.toPlainText()
        
        schedule_time = self.dt_picker.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        
        from src.storage.database.database import DatabaseManager
        db = DatabaseManager.get_instance()
        
        try:
            with db.get_connection() as conn:
                conn.execute(
                    "INSERT INTO scheduled_posts (video_path, title, description, platforms, schedule_time) VALUES (?, ?, ?, ?, ?)",
                    (video_path, title, desc, "YouTube Shorts, TikTok", schedule_time)
                )
                conn.commit()
            
            self.status_label.setText(f"Successfully scheduled for {schedule_time}!")
            self.status_label.setStyleSheet("color: #22C55E;")
        except Exception as e:
            self.status_label.setText(f"Database Error: {e}")
            self.status_label.setStyleSheet("color: #EF4444;")
