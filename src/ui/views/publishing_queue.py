import os
import json
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QListWidget, QPushButton, QTextEdit, QLineEdit, QSplitter,
    QCheckBox, QFrame
)
from PySide6.QtCore import Qt
from src.workers.base import BaseWorker
from PySide6.QtCore import QThreadPool
from PySide6.QtWidgets import QDialog

class PremiumWarningDialog(QDialog):
    def __init__(self, parent=None, platforms_str=""):
        super().__init__(parent)
        self.setWindowTitle("Action Required")
        self.setFixedSize(500, 230)
        self.setModal(True)
        
        from PySide6.QtCore import Qt
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        container = QWidget()
        container.setObjectName("container")
        container.setStyleSheet("""
            QWidget#container {
                background-color: #111827;
                border: 2px solid #374151;
                border-radius: 12px;
            }
            QLabel { color: #E5E7EB; }
        """)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(25, 25, 25, 25)
        container_layout.setSpacing(15)
        
        title_lbl = QLabel("⚠️ App Must Remain Open")
        title_lbl.setStyleSheet("color: #FBBF24; font-size: 18px; font-weight: bold;")
        container_layout.addWidget(title_lbl)
        
        msg_lbl = QLabel(f"You selected platforms ({platforms_str}) that do not support native cloud scheduling.\n\nNexus must remain running in the background at the exact scheduled time to publish these automatically.")
        msg_lbl.setWordWrap(True)
        msg_lbl.setStyleSheet("font-size: 14px; ")
        container_layout.addWidget(msg_lbl)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        btn_no = QPushButton("Cancel")
        btn_no.setFixedSize(100, 35)
        btn_no.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #4B5563;
                color: #D1D5DB;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #374151; }
        """)
        btn_no.clicked.connect(self.reject)
        
        btn_yes = QPushButton("I Understand")
        btn_yes.setFixedSize(140, 35)
        btn_yes.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #2563EB; }
        """)
        btn_yes.clicked.connect(self.accept)
        
        btn_layout.addWidget(btn_no)
        btn_layout.addWidget(btn_yes)
        container_layout.addLayout(btn_layout)
        
        main_layout.addWidget(container)

class PublishingQueueView(QWidget):
    def __init__(self):
        super().__init__()
        self.outputs_dir = Path("outputs")
        self.setup_ui()
        self.refresh_queue()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Publishing Queue")
        title.setProperty("class", "title")
        header_layout.addWidget(title)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setProperty("class", "secondary")
        refresh_btn.setFixedWidth(100)
        refresh_btn.clicked.connect(self.refresh_queue)
        
        clear_queue_btn = QPushButton("Clear Queue")
        clear_queue_btn.setStyleSheet("background-color: #EF4444; color: white; border-radius: 4px; padding: 6px 15px; font-weight: bold;")
        clear_queue_btn.setFixedWidth(120)
        clear_queue_btn.clicked.connect(self.clear_all_queue)
        
        header_layout.addWidget(refresh_btn)
        header_layout.addWidget(clear_queue_btn)
        
        main_layout.addLayout(header_layout)
        
        # Splitter for layout
        splitter = QSplitter(Qt.Orientation.Horizontal)
        from PySide6.QtWidgets import QSizePolicy
        splitter.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Left Panel (List of Videos)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        self.video_list = QListWidget()
        self.video_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.video_list.currentItemChanged.connect(self.on_video_selected)
        left_layout.addWidget(self.video_list)
        
        splitter.addWidget(left_panel)
        
        # Right Panel (Metadata Editor)
        self.right_panel = QWidget()
        right_layout = QVBoxLayout(self.right_panel)
        right_layout.setContentsMargins(10, 0, 0, 0)
        
        self.lbl_selected = QLabel("Select a video to prepare for publishing.")
        self.lbl_selected.setStyleSheet(" font-weight: bold;")
        right_layout.addWidget(self.lbl_selected)
        
        right_layout.addWidget(QLabel("Post Title:"))
        self.txt_title = QLineEdit()
        right_layout.addWidget(self.txt_title)
        
        right_layout.addWidget(QLabel("Description & Hashtags:"))
        self.txt_desc = QTextEdit()
        right_layout.addWidget(self.txt_desc)
        
        # ── Content Series Section (Phase 23) ──
        series_layout = QHBoxLayout()
        series_layout.addWidget(QLabel("Content Series:"))
        from PySide6.QtWidgets import QComboBox, QSpinBox
        self.cmb_series = QComboBox()
        self.cmb_series.addItem("None", None)
        self.cmb_series.addItem("+ Create New Series...", "NEW")
        self.cmb_series.currentIndexChanged.connect(self._on_series_changed)
        series_layout.addWidget(self.cmb_series)
        
        self.lbl_part = QLabel("Part #:")
        self.lbl_part.hide()
        series_layout.addWidget(self.lbl_part)
        
        self.spin_part = QSpinBox()
        self.spin_part.setMinimum(1)
        self.spin_part.setMaximum(999)
        self.spin_part.hide()
        self.spin_part.valueChanged.connect(self._on_part_changed)
        series_layout.addWidget(self.spin_part)
        series_layout.addStretch()
        
        right_layout.addLayout(series_layout)
        
        self._load_series_from_db()
        
        # Platform Selection
        platforms_group = QWidget()
        platforms_layout = QHBoxLayout(platforms_group)
        platforms_layout.setContentsMargins(0, 10, 0, 10)
        
        from PySide6.QtWidgets import QDateTimeEdit, QCheckBox
        from PySide6.QtCore import QDateTime
        
        self.chk_youtube = QCheckBox("YouTube Shorts")
        self.chk_youtube.setChecked(True)
        self.chk_tiktok = QCheckBox("TikTok")
        self.chk_instagram = QCheckBox("Instagram Reels")
        self.chk_facebook = QCheckBox("Facebook Reels")
        self.chk_twitter = QCheckBox("X (Twitter)")
        
        platforms_layout.addWidget(QLabel("Target Platforms:"))
        
        # Grid for checkboxes
        from PySide6.QtWidgets import QGridLayout
        chk_grid = QGridLayout()
        chk_grid.addWidget(self.chk_youtube, 0, 0)
        chk_grid.addWidget(self.chk_tiktok, 0, 1)
        chk_grid.addWidget(self.chk_instagram, 1, 0)
        chk_grid.addWidget(self.chk_facebook, 1, 1)
        chk_grid.addWidget(self.chk_twitter, 2, 0)
        
        platforms_layout.addLayout(chk_grid)
        platforms_layout.addStretch()
        right_layout.addWidget(platforms_group)
        
        # Schedule Time Picker
        time_layout = QHBoxLayout()
        time_layout.addWidget(QLabel("Publish Date/Time:"))
        
        self.dt_picker = QDateTimeEdit(QDateTime.currentDateTime().addSecs(2 * 3600))
        self.dt_picker.setMinimumDateTime(QDateTime.currentDateTime())
        self.dt_picker.setCalendarPopup(True)
        time_layout.addWidget(self.dt_picker)
        right_layout.addLayout(time_layout)
        
        # ── Give Credits to Nexus Toggle ──────────────────────────────────────
        credits_frame = QFrame()
        credits_frame.setObjectName("card")
        credits_frame.setStyleSheet(
            "QFrame#card { padding: 10px 14px; border-radius: 8px; }"
        )
        credits_row = QHBoxLayout(credits_frame)
        credits_row.setContentsMargins(0, 0, 0, 0)

        self.chk_credits = QCheckBox()
        self.chk_credits.setChecked(True)   # DEFAULT: ON for every video
        self.chk_credits.setFixedSize(20, 20)
        self.chk_credits.setStyleSheet("""
            QCheckBox::indicator { width: 18px; height: 18px; border-radius: 4px; border: 2px solid #3B82F6; background: transparent; }
            QCheckBox::indicator:checked { background-color: #3B82F6; border: 2px solid #3B82F6; image: none; }
            QCheckBox::indicator:checked::after { content: '✓'; }
        """)
        credits_row.addWidget(self.chk_credits)

        credits_lbl = QLabel("Give Credits to Nexus")
        credits_lbl.setStyleSheet("font-weight: 600; font-size: 13px; border: none;")
        credits_row.addWidget(credits_lbl)

        credits_sub = QLabel("— appends a branded line to the video description")
        credits_sub.setProperty("class", "subtitle")
        credits_sub.setStyleSheet("font-size: 11px; border: none;")
        credits_row.addWidget(credits_sub)

        credits_row.addStretch()

        badge = QLabel("Nexus ✦")
        badge.setStyleSheet(
            "background-color: #3B82F6; color: white; border-radius: 10px; "
            "padding: 2px 10px; font-size: 11px; font-weight: bold; border: none;"
        )
        credits_row.addWidget(badge)

        right_layout.addWidget(credits_frame)
        
        # Action Buttons
        btn_layout = QHBoxLayout()
        self.btn_ai = QPushButton("Generate Metadata (AI)")
        self.btn_ai.setProperty("class", "primary")
        self.btn_ai.clicked.connect(self.generate_metadata)
        btn_layout.addWidget(self.btn_ai)
        
        self.btn_schedule = QPushButton("Schedule Upload")
        self.btn_schedule.setProperty("class", "secondary")
        self.btn_schedule.clicked.connect(self.schedule_upload)
        btn_layout.addWidget(self.btn_schedule)
        
        self.btn_delete = QPushButton("Delete Clip")
        self.btn_delete.setStyleSheet("background-color: #EF4444; color: white; border-radius: 4px; padding: 6px 15px; font-weight: bold;")
        self.btn_delete.clicked.connect(self.delete_selected_clip)
        btn_layout.addWidget(self.btn_delete)
        
        right_layout.addLayout(btn_layout)
        self.right_panel.hide() # Hide until selected
        
        splitter.addWidget(self.right_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        main_layout.addWidget(splitter)
        
        main_layout.addSpacing(20)
        
        # Status
        self.status_label = QLabel("")
        main_layout.addWidget(self.status_label)

    def _load_series_from_db(self):
        from src.storage.database.database import DatabaseManager
        db = DatabaseManager.get_instance()
        with db.get_connection() as conn:
            cursor = conn.execute("SELECT id, name FROM content_series ORDER BY created_at DESC")
            # Keep first two items (None, Create New)
            while self.cmb_series.count() > 2:
                self.cmb_series.removeItem(2)
                
            for row in cursor.fetchall():
                self.cmb_series.addItem(row["name"], row["id"])
                
    def _on_series_changed(self, index):
        data = self.cmb_series.currentData()
        
        if data == "NEW":
            # Create new series
            from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
            
            class NewSeriesDialog(QDialog):
                def __init__(self, parent=None):
                    super().__init__(parent)
                    self.setWindowTitle("New Content Series")
                    self.setMinimumWidth(300)
                    self.setStyleSheet("QDialog { background-color: #F8FAFC; } QLabel { color: #0F172A; } QLineEdit { background-color: white; color: #0F172A; border: 1px solid #CBD5E1; border-radius: 4px; padding: 5px; }")
                    
                    layout = QVBoxLayout(self)
                    
                    lbl = QLabel("Enter series name (e.g. 'Gym Motivation Vlog'):")
                    layout.addWidget(lbl)
                    
                    self.txt_name = QLineEdit()
                    layout.addWidget(self.txt_name)
                    
                    btn_layout = QHBoxLayout()
                    btn_layout.addStretch()
                    
                    btn_cancel = QPushButton("Cancel")
                    btn_cancel.setStyleSheet("background-color: transparent; color: #64748B; border: none;")
                    btn_cancel.clicked.connect(self.reject)
                    
                    btn_create = QPushButton("Create Series")
                    btn_create.setProperty("class", "primary")
                    btn_create.setStyleSheet("background-color: #3B82F6; color: white; border-radius: 4px; padding: 6px 15px; font-weight: bold;")
                    btn_create.clicked.connect(self.accept)
                    
                    btn_layout.addWidget(btn_cancel)
                    btn_layout.addWidget(btn_create)
                    
                    layout.addLayout(btn_layout)
                    
            dialog = NewSeriesDialog(self)
            if dialog.exec() == QDialog.DialogCode.Accepted and dialog.txt_name.text().strip():
                text = dialog.txt_name.text().strip()
                from src.storage.database.database import DatabaseManager
                db = DatabaseManager.get_instance()
                with db.get_connection() as conn:
                    cursor = conn.execute("INSERT INTO content_series (name) VALUES (?) RETURNING id", (text.strip(),))
                    new_id = cursor.fetchone()[0]
                    conn.commit()
                self._load_series_from_db()
                # Find and select the new item
                idx = self.cmb_series.findData(new_id)
                if idx >= 0:
                    self.cmb_series.setCurrentIndex(idx)
            else:
                self.cmb_series.setCurrentIndex(0) # Reset to None
                return
                
        # Show/hide part number
        if self.cmb_series.currentData() not in (None, "NEW"):
            self.lbl_part.show()
            self.spin_part.show()
            # If the user checks the title, append "(Part X)" to title!
            title = self.txt_title.text()
            series_name = self.cmb_series.currentText()
            import re
            title = re.sub(r'\s*\(Part \d+\)', '', title)
            if title and series_name:
                self.txt_title.setText(f"{title} (Part {self.spin_part.value()})")
        else:
            self.lbl_part.hide()
            self.spin_part.hide()
            title = self.txt_title.text()
            import re
            self.txt_title.setText(re.sub(r'\s*\(Part \d+\)', '', title))

    def _on_part_changed(self):
        title = self.txt_title.text()
        import re
        title = re.sub(r'\s*\(Part \d+\)', '', title)
        if title:
            self.txt_title.setText(f"{title} (Part {self.spin_part.value()})")

    def refresh_queue(self):
        self.video_list.clear()
        if not self.outputs_dir.exists():
            return
            
        # Get all mp4 files and sort them by modification time, oldest first (so they match creation order)
        files = list(self.outputs_dir.glob("*.mp4"))
        files.sort(key=lambda f: f.stat().st_mtime, reverse=False)
            
        for file in files:
            from PySide6.QtWidgets import QListWidgetItem, QWidget, QVBoxLayout, QLabel
            from PySide6.QtCore import Qt
            
            item = QListWidgetItem(self.video_list)
            # Store filename in user role for retrieval
            item.setData(Qt.ItemDataRole.UserRole, file.name)
            
            card = QWidget()
            card.setObjectName("card")
            card.setStyleSheet("""
                QWidget#card {
                    background-color: transparent;
                }
            """)
            layout = QVBoxLayout(card)
            layout.setContentsMargins(10, 10, 10, 10)
            
            title = QLabel(file.name)
            title.setStyleSheet("font-weight: bold; font-size: 14px;")
            layout.addWidget(title)
            
            size_mb = file.stat().st_size / (1024 * 1024)
            meta = QLabel(f"Size: {size_mb:.1f} MB | MP4 Video")
            meta.setProperty("class", "subtitle")
            meta.setStyleSheet("font-size: 12px;")
            layout.addWidget(meta)
            
            from PySide6.QtCore import QSize
            item.setSizeHint(QSize(0, 95))
            self.video_list.addItem(item)
            self.video_list.setItemWidget(item, card)
            
    def on_video_selected(self, current, previous):
        if not current:
            self.right_panel.hide()
            return
            
        from PySide6.QtCore import Qt
        filename = current.data(Qt.ItemDataRole.UserRole)
        self.lbl_selected.setText(f"Preparing: {filename}")
        
        # Default title is the filename without .mp4 and without [DUPLICATE]
        default_title = Path(filename).stem.replace("[DUPLICATE] ", "").strip()
        self.txt_title.setText(default_title)
        self.txt_desc.clear()
        
        self.status_label.clear()
        self.chk_credits.setChecked(True)  # Reset to ON for every new video
        from PySide6.QtCore import QDateTime
        now = QDateTime.currentDateTime()
        self.dt_picker.setMinimumDateTime(now)                  # block past times
        self.dt_picker.setDateTime(now.addSecs(2 * 3600))       # default = now + 2h
        
        # Load existing JSON if we saved one
        json_file = self.outputs_dir / f"{Path(filename).stem}.json"
        if json_file.exists():
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.txt_title.setText(data.get('title', default_title))
                    self.txt_desc.setText(data.get('description', ''))
            except Exception:
                pass
                
        self.right_panel.show()

    def generate_metadata(self):
        item = self.video_list.currentItem()
        if not item:
            return
            
        from PySide6.QtCore import Qt
        filename = item.data(Qt.ItemDataRole.UserRole)
        clean_title = Path(filename).stem.replace("[DUPLICATE] ", "").strip()
        
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
        from PySide6.QtCore import Qt
        filename = self.video_list.currentItem().data(Qt.ItemDataRole.UserRole)
        clean_title = Path(filename).stem.replace("[DUPLICATE] ", "").strip()
        self.txt_title.setText(clean_title)
        self.txt_desc.setText(text)
        self.status_label.setText("Metadata generated! You can edit it manually before scheduling.")
        self.status_label.setStyleSheet("color: #22C55E;")
        
        # Save to JSON
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
            
        from PySide6.QtCore import Qt
        filename = item.data(Qt.ItemDataRole.UserRole)
        video_path = str((self.outputs_dir / filename).absolute())
        title = self.txt_title.text()
        desc = self.txt_desc.toPlainText()
        
        # ── Nexus Credits ─────────────────────────────────────────────────────
        # Appended silently to the final description — not shown in the editor.
        NORVI_CREDITS = (
            "\n\n—\n"
            "🎬 Clipped & published with Nexus\n"
            "Powered by Nexus Agency AI · nor-vi.in"
        )
        final_desc = desc + NORVI_CREDITS if self.chk_credits.isChecked() else desc
        
        # Read Platforms
        selected_platforms = []
        if self.chk_youtube.isChecked():
            selected_platforms.append("YouTube Shorts")
        if self.chk_tiktok.isChecked():
            selected_platforms.append("TikTok")
        if self.chk_instagram.isChecked():
            selected_platforms.append("Instagram Reels")
        if self.chk_facebook.isChecked():
            selected_platforms.append("Facebook")
        if self.chk_twitter.isChecked():
            selected_platforms.append("X")
            
        platforms_str = ", ".join(selected_platforms)
        if not platforms_str:
            self.status_label.setText("Error: Select at least one platform.")
            self.status_label.setStyleSheet("color: #EF4444;")
            return
            
        non_native = [p for p in selected_platforms if p in ("TikTok", "Instagram Reels", "X")]
        if non_native:
            from PySide6.QtWidgets import QDialog
            dialog = PremiumWarningDialog(self, ", ".join(non_native))
            if dialog.exec() == QDialog.DialogCode.Rejected:
                return
        
        schedule_time = self.dt_picker.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        
        from src.storage.database.database import DatabaseManager
        db = DatabaseManager.get_instance()
        
        try:
            with db.get_connection() as conn:
                # Check for previously published/scheduled instances of this video on selected platforms
                cursor = conn.execute(
                    "SELECT platforms FROM scheduled_posts WHERE video_path = ?",
                    (video_path,)
                )
                existing_platforms = []
                for row in cursor.fetchall():
                    existing_platforms.extend(row["platforms"].split(", "))
                    
                already_scheduled = [p for p in selected_platforms if p in existing_platforms]
                
                if already_scheduled:
                    from PySide6.QtWidgets import QMessageBox
                    msg = f"This video has already been scheduled or published to:\n\n{', '.join(already_scheduled)}\n\nAre you sure you want to schedule it again (which will result in duplicate uploads)?"
                    reply = QMessageBox.warning(self, "Duplicate Upload Warning", msg, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
                    if reply == QMessageBox.StandardButton.No:
                        return
                        
                # ── Prevent exact duplicate schedules ──
                # If this exact video is already scheduled at this exact time, block it.
                cursor = conn.execute(
                    "SELECT id FROM scheduled_posts WHERE video_path = ? AND schedule_time = ?",
                    (video_path, schedule_time)
                )
                if cursor.fetchone():
                    self.status_label.setText("Error: This video is already scheduled for this exact time!")
                    self.status_label.setStyleSheet("color: #EAB308;") # amber warning
                    return
                    
                conn.execute(
                    "INSERT INTO scheduled_posts (video_path, title, description, platforms, schedule_time) VALUES (?, ?, ?, ?, ?)",
                    (video_path, title, final_desc, platforms_str, schedule_time)
                )
                conn.commit()
            
            self.status_label.setText(f"Successfully scheduled for {schedule_time} on {platforms_str}!")
            self.status_label.setStyleSheet("color: #22C55E;")
        except Exception as e:
            self.status_label.setText(f"Database Error: {e}")
            self.status_label.setStyleSheet("color: #EF4444;")

    def delete_selected_clip(self):
        item = self.video_list.currentItem()
        if not item:
            return
            
        from PySide6.QtCore import Qt
        filename = item.data(Qt.ItemDataRole.UserRole)
        video_path = self.outputs_dir / filename
        
        if video_path.exists():
            import os
            try:
                os.remove(video_path)
            except Exception as e:
                self.status_label.setText(f"Failed to delete: {e}")
                self.status_label.setStyleSheet("color: #EF4444;")
                return
                
        self.refresh_queue()
        self.right_panel.hide()

    def clear_all_queue(self):
        import shutil
        if self.outputs_dir.exists():
            shutil.rmtree(self.outputs_dir, ignore_errors=True)
            self.outputs_dir.mkdir(exist_ok=True)
            
        self.status_label.setText("Queue completely cleared.")
        self.status_label.setStyleSheet("color: #22C55E;")
        self.refresh_queue()
        self.right_panel.hide()
