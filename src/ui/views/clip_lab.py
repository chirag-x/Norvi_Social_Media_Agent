from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QCheckBox, QFrame, QScrollArea
)
from PySide6.QtCore import Qt, QThreadPool
from src.app.state import AppState
from src.workers.base import BaseWorker

class ClipLabView(QWidget):
    """
    Clip Lab View where selected sources are analyzed.
    """
    def __init__(self):
        super().__init__()
        
        self.state = AppState.get_instance()
        self.state.active_source_changed.connect(self._on_source_changed)
        
        # Main Scroll Area
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        # Content Widget inside Scroll Area
        content_widget = QWidget()
        self.main_layout = QVBoxLayout(content_widget)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        scroll.setWidget(content_widget)
        
        # Base layout for the entire view
        base_layout = QVBoxLayout(self)
        base_layout.setContentsMargins(0, 0, 0, 0)
        base_layout.addWidget(scroll)
        
        title = QLabel("Clip Lab")
        title.setProperty("class", "title")
        self.main_layout.addWidget(title)
        
        # Container for when no source is selected
        self.empty_container = QWidget()
        empty_layout = QVBoxLayout(self.empty_container)
        empty_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_label = QLabel("No active source selected.\nGo to the Discover tab to find content.")
        empty_label.setProperty("class", "subtitle")
        empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_layout.addWidget(empty_label)
        self.main_layout.addWidget(self.empty_container)
        
        # Container for when a source is selected
        self.content_container = QWidget()
        content_layout = QVBoxLayout(self.content_container)
        
        # Source Details
        self.source_title = QLabel("")
        self.source_title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 5px;")
        content_layout.addWidget(self.source_title)
        
        self.source_meta = QLabel("")
        self.source_meta.setProperty("class", "subtitle")
        content_layout.addWidget(self.source_meta)
        
        # Fair Use Checklist
        checklist_frame = QFrame()
        checklist_frame.setObjectName("login_container") # Reusing the nice dark rounded box style
        check_layout = QVBoxLayout(checklist_frame)
        
        check_title = QLabel("Fair Use & Copyright Verification")
        check_title.setStyleSheet("font-weight: bold; font-size: 16px; margin-bottom: 10px;")
        check_layout.addWidget(check_title)
        
        self.chk_transformative = QCheckBox("I intend to add transformative value (commentary, criticism, education).")
        self.chk_commercial = QCheckBox("I understand the risks of commercializing unedited third-party content.")
        self.chk_credit = QCheckBox("I will provide proper credit/attribution to the original creator.")
        
        for chk in [self.chk_transformative, self.chk_commercial, self.chk_credit]:
            chk.setStyleSheet("margin-top: 5px; font-size: 14px;")
            chk.stateChanged.connect(self._validate_checklist)
            check_layout.addWidget(chk)
            
        content_layout.addWidget(checklist_frame)
        
        # Duration Selector (preset buttons, radio-style)
        self.selected_duration = 60  # default
        duration_layout = QHBoxLayout()
        duration_label = QLabel("Clip Duration:")
        duration_label.setProperty("class", "subtitle")
        duration_layout.addWidget(duration_label)
        
        self._duration_buttons = {}
        for seconds in [30, 60, 90, 120, 180]:
            label = f"{seconds}s"
            btn = QPushButton(label)
            btn.setFixedHeight(34)
            btn.setFixedWidth(72)
            btn.setCheckable(True)
            btn.setChecked(seconds == 60)
            btn.setProperty("class", "duration_btn")
            btn.clicked.connect(lambda checked, s=seconds: self._select_duration(s))
            self._duration_buttons[seconds] = btn
            duration_layout.addWidget(btn)
        
        duration_layout.addStretch()
        content_layout.addLayout(duration_layout)
        
        # Actions
        action_layout = QHBoxLayout()
        self.btn_analyze = QPushButton("Analyze with AI")
        self.btn_analyze.setProperty("class", "primary")
        self.btn_analyze.setFixedWidth(200)
        self.btn_analyze.setEnabled(False)
        self.btn_analyze.clicked.connect(self._start_analysis)
        action_layout.addWidget(self.btn_analyze)
        
        self.btn_stop = QPushButton("Stop")
        self.btn_stop.setStyleSheet("background-color: #EF4444; color: white; border-radius: 4px; padding: 6px 15px; font-weight: bold;")
        self.btn_stop.setFixedWidth(100)
        self.btn_stop.hide()
        self.btn_stop.clicked.connect(self._stop_analysis)
        action_layout.addWidget(self.btn_stop)
        
        action_layout.addStretch()
        content_layout.addLayout(action_layout)
        
        # Progress Tracking
        from PySide6.QtWidgets import QProgressBar
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(400)
        self.progress_bar.hide()
        
        self.status_label = QLabel("")
        self.status_label.setProperty("class", "subtitle")
        self.status_label.hide()
        
        self.main_layout.addWidget(self.content_container)
        
        # Add to base layout so it is sticky at bottom
        base_layout.addWidget(self.progress_bar)
        base_layout.addWidget(self.status_label)
        
        self._update_ui()

    def _on_source_changed(self, video):
        self._update_ui()
        
    def _update_ui(self):
        video = self.state.active_source
        if video:
            self.empty_container.hide()
            self.content_container.show()
            self.source_title.setText(video.title)
            self.source_meta.setText(f"Channel: {video.channel} | URL: {video.url}")
            
            # Reset checklist
            self.chk_transformative.setChecked(False)
            self.chk_commercial.setChecked(False)
            self.chk_credit.setChecked(False)
            self.btn_analyze.setEnabled(False)
        else:
            self.empty_container.show()
            self.content_container.hide()
            
    def _validate_checklist(self):
        if (self.chk_transformative.isChecked() and 
            self.chk_commercial.isChecked() and 
            self.chk_credit.isChecked()):
            self.btn_analyze.setEnabled(True)
        else:
            self.btn_analyze.setEnabled(False)
            
    def _select_duration(self, seconds: int):
        """Handle duration preset button selection (radio-style)."""
        self.selected_duration = seconds
        for s, btn in self._duration_buttons.items():
            btn.setChecked(s == seconds)
            
    def _start_analysis(self):
        video = self.state.active_source
        if not video: return
        
        self._is_cancelled = False
        self.btn_analyze.setEnabled(False)
        self.btn_stop.show()
        self.progress_bar.show()
        self.progress_bar.setValue(0)
        self.status_label.setText("Preparing media...")
        self.status_label.show()
        
        # We need a worker with custom signals for progress
        import asyncio
            
        self.media_worker = BaseWorker(self._async_download)
        self.media_worker.signals.progress_msg.connect(self._on_download_progress)
        self.media_worker.signals.result.connect(self._on_download_success)
        self.media_worker.signals.error.connect(self._on_download_error)
        
        QThreadPool.globalInstance().start(self.media_worker)

    def _async_download(self, progress_callback=None):
        from src.services.media.downloader import MediaProcessor
        import asyncio
        
        def _progress_bridge(percent, msg):
            if getattr(self, '_is_cancelled', False):
                raise InterruptedError("Cancelled by user")
            if self.media_worker and hasattr(self.media_worker.signals, 'progress_msg'):
                self.media_worker.signals.progress_msg.emit(percent, msg)
                
        processor = MediaProcessor()
        return asyncio.run(processor.download_and_prepare(
            self.state.active_source.url,
            self.state.active_source.title,
            progress_callback=_progress_bridge
        ))
        
    def _on_download_progress(self, percent: int, msg: str):
        self.progress_bar.setValue(percent)
        self.status_label.setText(msg)
        
    def _on_download_success(self, paths: dict):
        self.status_label.setText(f"Media Ready! Starting Transcription...")
        self.status_label.setStyleSheet("color: #EAB308; font-weight: bold;") # Yellow for working
        
        # Now start transcription in a new worker
        self.transcribe_worker = BaseWorker(self._async_transcribe, paths['audio'])
        self.transcribe_worker.signals.progress_msg_str.connect(self._on_transcribe_progress)
        self.transcribe_worker.signals.result.connect(self._on_transcribe_success)
        self.transcribe_worker.signals.error.connect(self._on_download_error)
        
        QThreadPool.globalInstance().start(self.transcribe_worker)
        
    def _async_transcribe(self, audio_path: str, progress_callback=None):
        from src.services.ai.transcriber import WhisperTranscriber
        import asyncio
        
        def _progress_bridge(msg):
            if getattr(self, '_is_cancelled', False):
                raise InterruptedError("Cancelled by user")
            if self.transcribe_worker and hasattr(self.transcribe_worker.signals, 'progress_msg_str'):
                self.transcribe_worker.signals.progress_msg_str.emit(msg)
                
        transcriber = WhisperTranscriber.get_instance()
        return asyncio.run(transcriber.transcribe(audio_path, progress_callback=_progress_bridge))
        
    def _on_transcribe_progress(self, msg: str):
        self.status_label.setText(msg)
        
    def _on_transcribe_success(self, transcript: list):
        self.progress_bar.setValue(100)
        self.status_label.setText("Transcription Complete! Sending to Gemma AI for analysis...")
        self.status_label.setStyleSheet("color: #EAB308; font-weight: bold;")
        
        # Save transcript to state
        self.state.transcript = transcript
        
        # Start Gemma Worker
        self.gemma_worker = BaseWorker(self._async_gemma_analysis, transcript)
        self.gemma_worker.signals.result.connect(self._on_gemma_success)
        self.gemma_worker.signals.error.connect(self._on_download_error)
        
        from PySide6.QtCore import QThreadPool
        QThreadPool.globalInstance().start(self.gemma_worker)

    def _async_gemma_analysis(self, transcript: list):
        from src.services.ai.gemma_engine import GemmaEngine
        import asyncio
        
        engine = GemmaEngine.get_instance()
        
        context = {
            "title": self.state.active_source.title,
            "niche": self.state.active_source.niche
        }
        
        max_dur = getattr(self, 'selected_duration', 60)
        return asyncio.run(engine.analyze_transcript(transcript, context, max_clip_duration=max_dur))

    def _on_gemma_success(self, clips: list):
        self.btn_stop.hide()
        self.btn_analyze.setEnabled(True)
        self.status_label.setText(f"Analysis Complete! Found {len(clips)} viral clips.")
        self.status_label.setStyleSheet("color: #22C55E; font-weight: bold;")
        
        # Duplicate Detection (Phase 22)
        try:
            from src.storage.database.database import DatabaseManager
            db = DatabaseManager.get_instance()
            with db.get_connection() as conn:
                cursor = conn.execute("SELECT start_time, end_time FROM extracted_clips WHERE source_video_id = ?", (self.state.active_source.id,))
                past_clips = cursor.fetchall()
                
                for clip in clips:
                    c_start = clip.get('start_time', 0.0)
                    c_end = clip.get('end_time', 0.0)
                    clip['is_duplicate'] = False
                    
                    for past in past_clips:
                        # If start times are within 15 seconds of each other, it's basically the same clip
                        if abs(c_start - past['start_time']) < 15.0:
                            clip['is_duplicate'] = True
                            clip['title'] = "[DUPLICATE] " + clip.get('title', '')
                            break
        except Exception as e:
            print(f"Duplicate detection failed: {e}")
        
        # Store clips in global state
        self.state.extracted_clips = clips
        
        self._render_clips(clips)

    def _render_clips(self, clips: list):
        # Clear existing clip UI if any
        if hasattr(self, 'clips_container'):
            self.clips_container.deleteLater()
            
        self.clips_container = QWidget()
        clips_layout = QVBoxLayout(self.clips_container)
        clips_layout.setContentsMargins(0, 20, 0, 0)
        
        title_label = QLabel("Generated Viral Clips")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        clips_layout.addWidget(title_label)
        
        # Sort by start_time ascending (chronological order)
        clips.sort(key=lambda x: x.get('start_time', 0))
        
        for i, clip in enumerate(clips):
            card = QFrame()
            card.setObjectName("card")
            
            is_dup = clip.get('is_duplicate', False)
            if is_dup:
                card.setStyleSheet("QFrame#card { border: 2px solid #EF4444; }")
                
            card_layout = QVBoxLayout(card)
            
            # Header: Title and Score
            header_layout = QHBoxLayout()
            title = QLabel(f"🔥 {clip.get('title', 'Viral Clip')}")
            if is_dup:
                title.setStyleSheet("font-size: 16px; font-weight: bold; color: #EF4444; border: none;")
            else:
                title.setStyleSheet("font-size: 16px; font-weight: bold; color: #3B82F6; border: none;")
            header_layout.addWidget(title)
            
            score = QLabel(f"Score: {clip.get('virality_score', 0)}/10")
            score.setStyleSheet("font-weight: bold; color: #EAB308; border: none;")
            header_layout.addWidget(score)
            card_layout.addLayout(header_layout)
            
            # Timestamps
            time_label = QLabel(f"⏱️ {clip.get('start_time', 0)}s - {clip.get('end_time', 0)}s")
            time_label.setProperty("class", "subtitle")
            time_label.setStyleSheet("border: none;")
            card_layout.addWidget(time_label)
            
            # Reasoning
            reason_text = clip.get('reasoning', 'No reasoning provided.')
            if is_dup:
                reason_text = "WARNING: You already extracted this exact segment from this video previously! Generating it again will result in a duplicate video.\n\n" + reason_text
                
            reason = QLabel(reason_text)
            reason.setWordWrap(True)
            reason.setProperty("class", "subtitle")
            reason.setStyleSheet("margin-top: 10px; border: none;")
            card_layout.addWidget(reason)
            
            # Actions
            btn_layout = QHBoxLayout()
            
            btn_preview = QPushButton("Preview Clip")
            btn_preview.setStyleSheet("""
                QPushButton {
                    background-color: transparent; 
                    color: #38BDF8; 
                    border: 1px solid #38BDF8; 
                    border-radius: 4px;
                    padding: 5px 15px;
                }
                QPushButton:hover { background-color: rgba(56, 189, 248, 0.1); }
            """)
            btn_preview.clicked.connect(lambda checked, c=clip: self._preview_clip(c))
            btn_layout.addWidget(btn_preview)
            
            btn_layout.addStretch()
            
            btn_reject = QPushButton("Reject")
            btn_reject.setStyleSheet("""
                QPushButton {
                    background-color: transparent; 
                    color: #EF4444; 
                    border: 1px solid #EF4444; 
                    border-radius: 4px;
                    padding: 5px 15px;
                }
                QPushButton:hover { background-color: rgba(239, 68, 68, 0.1); }
            """)
            btn_reject.clicked.connect(lambda checked, f=card: f.hide())
            btn_layout.addWidget(btn_reject)
            
            btn_approve = QPushButton("Approve to Queue")
            if is_dup:
                btn_approve.setStyleSheet("""
                    QPushButton {
                        background-color: #22C55E; 
                        color: white; 
                        border-radius: 4px;
                        padding: 5px 15px; 
                        font-weight: bold;
                    }
                    QPushButton:hover { background-color: #16A34A; }
                """)
                btn_approve.clicked.connect(lambda checked, c=clip, f=card, btn=btn_approve: self._approve_duplicate(c, f, btn))
            else:
                btn_approve.setStyleSheet("""
                    QPushButton {
                        background-color: #22C55E; 
                        color: white; 
                        border-radius: 4px;
                        padding: 5px 15px; 
                        font-weight: bold;
                    }
                    QPushButton:hover { background-color: #16A34A; }
                """)
                btn_approve.clicked.connect(lambda checked, c=clip, f=card, btn=btn_approve: self._approve_clip(c, f, btn))
            
            btn_layout.addWidget(btn_approve)
            
            card_layout.addLayout(btn_layout)
            clips_layout.addWidget(card)
            
        clips_layout.addStretch() # Pushes cards to the top
        self.main_layout.addWidget(self.clips_container)
        
    def _preview_clip(self, clip_data: dict):
        from src.services.media.downloader import MediaProcessor
        from src.ui.components.video_player import PreviewDialog
        
        processor = MediaProcessor()
        safe_title = processor._sanitize_filename(self.state.active_source.title)
        source_video = processor.cache_dir / f"{safe_title}.mp4"
        
        if not source_video.exists():
            self.status_label.setText("Error: Source video not found in cache.")
            self.status_label.setStyleSheet("color: #EF4444;")
            self.status_label.show()
            return
            
        dialog = PreviewDialog(
            str(source_video), 
            clip_data.get('start_time', 0.0), 
            clip_data.get('end_time', 0.0),
            self
        )
        dialog.exec()
        
    def _approve_duplicate(self, clip_data: dict, card, btn):
        """Show a styled confirmation before approving a duplicate clip."""
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
        from PySide6.QtCore import Qt
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Duplicate Clip")
        dialog.setFixedSize(460, 200)
        dialog.setModal(True)
        
        outer = QVBoxLayout(dialog)
        outer.setContentsMargins(0, 0, 0, 0)
        
        container = QWidget()
        container.setObjectName("dup_dialog")
        container.setStyleSheet("""
            QWidget#dup_dialog {
                background-color: #111827;
                border-radius: 12px;
            }
        """)
        vbox = QVBoxLayout(container)
        vbox.setContentsMargins(28, 24, 28, 24)
        vbox.setSpacing(14)
        
        # Icon + title row
        title_row = QHBoxLayout()
        icon_lbl = QLabel("⚠️")
        icon_lbl.setStyleSheet("font-size: 24px; border: none;")
        title_row.addWidget(icon_lbl)
        
        title_lbl = QLabel("Already Extracted")
        title_lbl.setStyleSheet("color: #FBBF24; font-size: 17px; font-weight: bold; border: none;")
        title_row.addWidget(title_lbl)
        title_row.addStretch()
        vbox.addLayout(title_row)
        
        # Message
        msg = QLabel("This clip was already extracted from this video once.\nApproving again will create a duplicate in your queue.")
        msg.setWordWrap(True)
        msg.setStyleSheet("color: #9CA3AF; font-size: 13px; border: none; line-height: 1.5;")
        vbox.addWidget(msg)
        
        vbox.addStretch()
        
        # Buttons
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        
        btn_cancel = QPushButton("Cancel")
        btn_cancel.setFixedSize(110, 36)
        btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #4B5563;
                color: #D1D5DB;
                border-radius: 8px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover { border-color: #6B7280; color: white; }
        """)
        btn_cancel.clicked.connect(dialog.reject)
        btn_row.addWidget(btn_cancel)
        
        btn_ok = QPushButton("Approve Anyway")
        btn_ok.setFixedSize(140, 36)
        btn_ok.setStyleSheet("""
            QPushButton {
                background-color: #22C55E;
                color: white;
                border-radius: 8px;
                font-size: 13px;
                font-weight: 700;
                border: none;
            }
            QPushButton:hover { background-color: #16A34A; }
        """)
        btn_ok.clicked.connect(dialog.accept)
        btn_row.addWidget(btn_ok)
        vbox.addLayout(btn_row)
        
        outer.addWidget(container)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._approve_clip(clip_data, card, btn)

    def _approve_clip(self, clip_data: dict, card, btn: QPushButton):
        btn.setText("Saved to outputs!")
        btn.setStyleSheet("background-color: #374151; color: #9CA3AF; border-radius: 4px; padding: 5px 15px; font-weight: bold;")
        btn.setEnabled(False)
        
        self.status_label.setText(f"Queuing: {clip_data.get('title')} for rendering...")
        self.status_label.setStyleSheet("color: #38BDF8; font-weight: bold; font-size: 14px; padding: 10px;")
        self.status_label.show()
        
        # Here we will kick off Phase 14 Video rendering
        from src.workers.base import BaseWorker
        from PySide6.QtCore import QThreadPool
        
        worker = BaseWorker(self._async_render_clip, clip_data)
        worker.signals.result.connect(self._on_render_success)
        worker.signals.error.connect(self._on_download_error)
        QThreadPool.globalInstance().start(worker)
        
    def _async_render_clip(self, clip_data: dict):
        from src.services.media.renderer import VideoRenderer
        import asyncio
        
        # We need the original downloaded video path. It's in the cache folder.
        from src.services.media.downloader import MediaProcessor
        processor = MediaProcessor()
        safe_title = processor._sanitize_filename(self.state.active_source.title)
        source_video = processor.cache_dir / f"{safe_title}.mp4"
        
        renderer = VideoRenderer()
        output_path = asyncio.run(renderer.extract_clip(
            str(source_video),
            clip_data.get('start_time', 0.0),
            clip_data.get('end_time', 0.0),
            clip_data.get('title', 'viral_clip'),
            crop_vertical=True,
            transcript=self.state.transcript
        ))
        return (output_path, clip_data)
        
    def _on_render_success(self, result: tuple):
        output_path, clip_data = result
        self.status_label.setText(f"Success! Video saved to: {output_path}")
        self.status_label.setStyleSheet("color: #22C55E; font-weight: bold;")
        
        # Save to extracted_clips database to prevent duplicates later (Phase 22)
        try:
            from src.storage.database.database import DatabaseManager
            db = DatabaseManager.get_instance()
            with db.get_connection() as conn:
                conn.execute(
                    "INSERT INTO extracted_clips (source_video_id, start_time, end_time, clip_title) VALUES (?, ?, ?, ?)",
                    (self.state.active_source.id, clip_data.get('start_time', 0.0), clip_data.get('end_time', 0.0), clip_data.get('title', 'unknown'))
                )
                conn.commit()
        except Exception as e:
            print(f"Failed to log extracted clip: {e}")        
    def _stop_analysis(self):
        self._is_cancelled = True
        self.btn_stop.hide()
        self.btn_analyze.setEnabled(True)
        self.status_label.setText("Analysis cancelled.")
        self.status_label.setStyleSheet("color: #EF4444;")
        self.progress_bar.hide()

    def _on_download_error(self, err):
        self.btn_stop.hide()
        self.btn_analyze.setEnabled(True)
        if "Cancelled by user" in str(err):
            self.status_label.setText("Analysis cancelled.")
        else:
            self.status_label.setText(f"Error: {err[1]}")
        self.status_label.setStyleSheet("color: #EF4444; font-weight: bold;")
