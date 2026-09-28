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
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
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
        
        # Duration Selector
        from PySide6.QtWidgets import QSpinBox
        duration_layout = QHBoxLayout()
        duration_label = QLabel("Clip Duration (seconds):")
        duration_label.setProperty("class", "subtitle")
        duration_layout.addWidget(duration_label)
        
        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(10, 120)
        self.duration_spin.setValue(60)
        self.duration_spin.setFixedWidth(100)
        self.duration_spin.setStyleSheet("background-color: #171C26; color: #F5F7FA; border: 1px solid #70798A; padding: 5px;")
        duration_layout.addWidget(self.duration_spin)
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
        
        self.btn_clear_cache = QPushButton("Clear Cache")
        self.btn_clear_cache.setFixedWidth(120)
        self.btn_clear_cache.clicked.connect(self._clear_cache)
        action_layout.addWidget(self.btn_clear_cache)
        
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
        
        return asyncio.run(engine.analyze_transcript(transcript, context))

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
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        clips_layout.addWidget(title_label)
        
        # Sort by virality score descending
        clips.sort(key=lambda x: x.get('virality_score', 0), reverse=True)
        
        for i, clip in enumerate(clips):
            card = QFrame()
            
            is_dup = clip.get('is_duplicate', False)
            if is_dup:
                card.setStyleSheet("background-color: #1E293B; border: 2px solid #EF4444; border-radius: 8px; padding: 15px;")
            else:
                card.setStyleSheet("background-color: #1E293B; border-radius: 8px; padding: 15px;")
                
            card_layout = QVBoxLayout(card)
            
            # Header: Title and Score
            header_layout = QHBoxLayout()
            title = QLabel(f"🔥 {clip.get('title', 'Viral Clip')}")
            if is_dup:
                title.setStyleSheet("font-size: 16px; font-weight: bold; color: #EF4444; border: none;")
            else:
                title.setStyleSheet("font-size: 16px; font-weight: bold; color: #38BDF8; border: none;")
            header_layout.addWidget(title)
            
            score = QLabel(f"Score: {clip.get('virality_score', 0)}/10")
            score.setStyleSheet("font-weight: bold; color: #EAB308; border: none;")
            header_layout.addWidget(score)
            card_layout.addLayout(header_layout)
            
            # Timestamps
            time_label = QLabel(f"⏱️ {clip.get('start_time', 0)}s - {clip.get('end_time', 0)}s")
            time_label.setStyleSheet("color: #94A3B8; border: none;")
            card_layout.addWidget(time_label)
            
            # Reasoning
            reason_text = clip.get('reasoning', 'No reasoning provided.')
            if is_dup:
                reason_text = "WARNING: You already extracted this exact segment from this video previously! Generating it again will result in a duplicate video.\n\n" + reason_text
                
            reason = QLabel(reason_text)
            reason.setWordWrap(True)
            reason.setStyleSheet("color: #CBD5E1; margin-top: 10px; border: none;")
            card_layout.addWidget(reason)
            
            # Actions
            btn_layout = QHBoxLayout()
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
                btn_approve.setEnabled(False)
                btn_approve.setText("Already Extracted")
                btn_approve.setStyleSheet("""
                    QPushButton {
                        background-color: #475569; 
                        color: #94A3B8; 
                        border-radius: 4px;
                        padding: 5px 15px; 
                        font-weight: bold;
                    }
                """)
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
            
            # Pass clip data to approval function
            btn_approve.clicked.connect(lambda checked, c=clip, f=card, btn=btn_approve: self._approve_clip(c, f, btn))
            btn_layout.addWidget(btn_approve)
            
            card_layout.addLayout(btn_layout)
            clips_layout.addWidget(card)
            
        clips_layout.addStretch() # Pushes cards to the top
        self.main_layout.addWidget(self.clips_container)
        
    def _approve_clip(self, clip_data: dict, card: QFrame, btn: QPushButton):
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

    def _clear_cache(self):
        import shutil
        from pathlib import Path
        
        # Clear temporary downloaded videos
        cache_dir = Path("cache")
        if cache_dir.exists():
            shutil.rmtree(cache_dir)
            cache_dir.mkdir()
            
        # Clear rendered video clips
        outputs_dir = Path("outputs")
        if outputs_dir.exists():
            shutil.rmtree(outputs_dir)
            outputs_dir.mkdir()
            
        self.status_label.setText("Cache and output files cleared successfully.")
        self.status_label.setStyleSheet("color: #22C55E; font-weight: bold;")
        self.status_label.show()

    def _on_download_error(self, err):
        self.btn_stop.hide()
        self.btn_analyze.setEnabled(True)
        if "Cancelled by user" in str(err):
            self.status_label.setText("Analysis cancelled.")
        else:
            self.status_label.setText(f"Error: {err[1]}")
        self.status_label.setStyleSheet("color: #EF4444; font-weight: bold;")
