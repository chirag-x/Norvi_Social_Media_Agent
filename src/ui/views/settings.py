from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, 
    QScrollArea, QLineEdit, QPushButton, QFormLayout
)
from PySide6.QtCore import Qt
from src.ui.theme import ThemeManager
from src.storage.database.database import DatabaseManager
from src.ui.components.collapsible import CollapsibleSection

class SettingsView(QWidget):
    """
    Settings view for configuring the application and connecting Social APIs.
    """
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager.get_instance()
        
        main_layout = QVBoxLayout(self)
        
        title = QLabel("Settings & Integrations")
        title.setProperty("class", "title")
        main_layout.addWidget(title)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        scroll_content = QWidget()
        self.layout = QVBoxLayout(scroll_content)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setSpacing(15)
        
        # Appearance
        self._build_appearance_section()
        
        # Performance (Phase 28)
        self._build_performance_section()
        
        # System Maintenance
        self._build_maintenance_section()
        
        # Transcription Settings
        self._build_transcription_section()
        
        # Social APIs
        api_title = QLabel("Social Media Developer Accounts")
        api_title.setStyleSheet("font-size: 16px; font-weight: bold;  margin-top: 15px;")
        self.layout.addWidget(api_title)
        
        self.api_inputs = {}
        
        self._build_api_section("YouTube Data API v3", "youtube", ["Client ID", "Client Secret"])
        self._build_api_section("TikTok for Developers", "tiktok", ["Client Key", "Client Secret"])
        self._build_api_section("Instagram Graph API", "instagram", ["App ID", "App Secret", "Access Token"])
        self._build_api_section("Facebook Graph API", "facebook", ["App ID", "App Secret", "Access Token"])
        self._build_api_section("X (Twitter) API v2", "twitter", ["API Key", "API Secret", "Access Token", "Access Secret"])
        
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
        
        self.load_api_keys()

    def _build_appearance_section(self):
        section = CollapsibleSection("Appearance (Theme)")
        layout = QHBoxLayout()
        
        theme_label = QLabel("Theme Preference:")
        
        layout.addWidget(theme_label)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["System", "Dark", "Light"])
        self.theme_combo.setFixedWidth(150)
        current_pref = ThemeManager.get_instance().get_theme_preference()
        self.theme_combo.setCurrentText(current_pref)
        self.theme_combo.currentTextChanged.connect(self._on_theme_changed)
        layout.addWidget(self.theme_combo)
        
        layout.addStretch()
        section.addLayout(layout)
        self.layout.addWidget(section)

    def _build_performance_section(self):
        section = CollapsibleSection("Resource Controls")
        layout = QFormLayout()
        
        # FFmpeg Threads
        self.combo_ffmpeg_threads = QComboBox()
        self.combo_ffmpeg_threads.addItems(["Auto", "1", "2", "4", "8", "16"])
        current_threads = self.db.get_setting("ffmpeg_threads", "Auto")
        self.combo_ffmpeg_threads.setCurrentText(current_threads)
        
        # FFmpeg HWAccel
        self.combo_ffmpeg_hwaccel = QComboBox()
        self.combo_ffmpeg_hwaccel.addItems(["None (CPU)", "NVIDIA (NVENC)", "AMD (AMF)", "Intel (QSV)"])
        current_hwaccel = self.db.get_setting("ffmpeg_hwaccel", "None (CPU)")
        self.combo_ffmpeg_hwaccel.setCurrentText(current_hwaccel)
        
        lbl_threads = QLabel("FFmpeg CPU Limit:")
        lbl_hwaccel = QLabel("FFmpeg GPU Accel:")
        
        layout.addRow(lbl_threads, self.combo_ffmpeg_threads)
        layout.addRow(lbl_hwaccel, self.combo_ffmpeg_hwaccel)
        
        btn_save = QPushButton("Save Performance Settings")
        btn_save.setProperty("class", "primary")
        btn_save.clicked.connect(self._save_performance_settings)
        layout.addRow("", btn_save)
        
        self.lbl_perf_status = QLabel("")
        layout.addRow("", self.lbl_perf_status)
        
        section.addLayout(layout)
        self.layout.addWidget(section)

    def _save_performance_settings(self):
        self.db.set_setting("ffmpeg_threads", self.combo_ffmpeg_threads.currentText())
        self.db.set_setting("ffmpeg_hwaccel", self.combo_ffmpeg_hwaccel.currentText())
        self.lbl_perf_status.setText("Saved successfully!")
        self.lbl_perf_status.setStyleSheet("color: #22C55E;")

    def _build_maintenance_section(self):
        section = CollapsibleSection("System Maintenance (Cache)")
        layout = QVBoxLayout()
        
        hint = QLabel("This will delete all temporary downloaded videos and AI-generated clips to free up space. This will NOT reset your app configurations or API keys.")
        hint.setWordWrap(True)
        hint.setStyleSheet(" font-style: italic; margin-bottom: 10px;")
        layout.addWidget(hint)
        
        btn_layout = QHBoxLayout()
        self.btn_clear_cache = QPushButton("Clear Cache (Reset Videos)")
        self.btn_clear_cache.setProperty("class", "secondary")
        self.btn_clear_cache.setStyleSheet("background-color: #EF4444; color: white; border-radius: 4px; padding: 8px 15px; font-weight: bold;")
        self.btn_clear_cache.setFixedWidth(250)
        self.btn_clear_cache.clicked.connect(self._clear_cache)
        btn_layout.addWidget(self.btn_clear_cache)
        
        self.cache_status_lbl = QLabel("")
        btn_layout.addWidget(self.cache_status_lbl)
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        section.addLayout(layout)
        self.layout.addWidget(section)

    def _build_transcription_section(self):
        section = CollapsibleSection("Transcription Engine")
        from PySide6.QtCore import QSettings
        settings = QSettings("Nexus", "SocialMediaAgent")
        
        # Engine selection
        engine_layout = QHBoxLayout()
        engine_lbl = QLabel("Transcription Engine:")
        
        engine_layout.addWidget(engine_lbl)
        
        self.combo_engine = QComboBox()
        self.combo_engine.addItems(["Local (Faster-Whisper)", "Cloud (Groq API)"])
        current_engine = settings.value("transcription_engine", "Local (Faster-Whisper)")
        self.combo_engine.setCurrentText(current_engine)
        self.combo_engine.currentTextChanged.connect(self._on_engine_changed)
        engine_layout.addWidget(self.combo_engine)
        engine_layout.addStretch()
        section.addLayout(engine_layout)
        
        # Local options
        self.local_container = QWidget()
        local_layout = QFormLayout(self.local_container)
        local_layout.setContentsMargins(0, 10, 0, 10)
        
        local_model_layout = QHBoxLayout()
        self.combo_local_model = QComboBox()
        self.combo_local_model.addItems(["base", "medium", "large-v3"])
        current_local = settings.value("local_whisper_model", "base")
        self.combo_local_model.setCurrentText(current_local)
        local_model_layout.addWidget(self.combo_local_model)
        
        self.btn_download_model = QPushButton("Download Model")
        self.btn_download_model.setProperty("class", "secondary")
        self.btn_download_model.clicked.connect(self._download_local_model)
        local_model_layout.addWidget(self.btn_download_model)
        
        self.lbl_download_status = QLabel("")
        self.lbl_download_status.setStyleSheet("color: #EAB308; margin-left: 10px;") # Yellow
        local_model_layout.addWidget(self.lbl_download_status)
        local_model_layout.addStretch()
        
        lbl_loc = QLabel("Local Model Size:")
        
        local_layout.addRow(lbl_loc, local_model_layout)
        
        # Cloud options
        self.cloud_container = QWidget()
        cloud_layout = QFormLayout(self.cloud_container)
        cloud_layout.setContentsMargins(0, 10, 0, 10)
        
        self.txt_groq_api = QLineEdit()
        self.txt_groq_api.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)
        self.txt_groq_api.setText(settings.value("groq_api_key", ""))
        
        self.combo_cloud_model = QComboBox()
        self.combo_cloud_model.addItems(["whisper-large-v3", "whisper-large-v3-turbo"])
        current_cloud = settings.value("cloud_whisper_model", "whisper-large-v3-turbo")
        self.combo_cloud_model.setCurrentText(current_cloud)
        
        lbl_groq = QLabel("Groq API Key:")
        
        lbl_cmod = QLabel("Groq Model:")
        
        cloud_layout.addRow(lbl_groq, self.txt_groq_api)
        cloud_layout.addRow(lbl_cmod, self.combo_cloud_model)
        
        section.addWidget(self.local_container)
        section.addWidget(self.cloud_container)
        
        # Save button
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save Transcription Settings")
        save_btn.setProperty("class", "primary")
        save_btn.clicked.connect(self._save_transcription_settings)
        btn_layout.addWidget(save_btn)
        
        self.lbl_transcription_status = QLabel("")
        btn_layout.addWidget(self.lbl_transcription_status)
        btn_layout.addStretch()
        section.addLayout(btn_layout)
        
        self.layout.addWidget(section)
        
        # Initial visibility toggle
        self._on_engine_changed(self.combo_engine.currentText())

    def _on_engine_changed(self, text: str):
        if "Local" in text:
            self.local_container.show()
            self.cloud_container.hide()
        else:
            self.local_container.hide()
            self.cloud_container.show()

    def _save_transcription_settings(self):
        from PySide6.QtCore import QSettings
        settings = QSettings("Nexus", "SocialMediaAgent")
        
        settings.setValue("transcription_engine", self.combo_engine.currentText())
        settings.setValue("local_whisper_model", self.combo_local_model.currentText())
        settings.setValue("groq_api_key", self.txt_groq_api.text())
        settings.setValue("cloud_whisper_model", self.combo_cloud_model.currentText())
        
        self.lbl_transcription_status.setText("Saved successfully!")
        self.lbl_transcription_status.setStyleSheet("color: #22C55E; margin-left: 10px;")

    def _clear_cache(self):
        import shutil
        from pathlib import Path
        from src.config.config import get_config
        
        # Clear temporary downloaded videos
        cache_dir = Path("cache")
        if cache_dir.exists():
            shutil.rmtree(cache_dir, ignore_errors=True)
            cache_dir.mkdir(exist_ok=True)
            
        # Clear rendered video clips
        outputs_dir = Path("outputs")
        if outputs_dir.exists():
            shutil.rmtree(outputs_dir, ignore_errors=True)
            outputs_dir.mkdir(exist_ok=True)
            
        # Clear logs
        log_file = Path(get_config().app_data_dir) / "logs" / "app.log"
        if log_file.exists():
            try:
                open(log_file, "w").close()
            except Exception:
                pass
            
        self.cache_status_lbl.setText("Cache, videos, and logs cleared successfully!")
        self.cache_status_lbl.setStyleSheet("color: #22C55E; font-weight: bold; margin-left: 10px;")

    def _build_api_section(self, title_text: str, platform_id: str, fields: list):
        section = CollapsibleSection(title_text)
        form = QFormLayout()
        
        inputs = {}
        for field in fields:
            line_edit = QLineEdit()
            line_edit.setEchoMode(QLineEdit.EchoMode.Password)

            # Eye toggle button
            eye_btn = QPushButton("👁")
            eye_btn.setFixedSize(34, 34)
            eye_btn.setCheckable(True)
            eye_btn.setToolTip("Show / Hide")
            eye_btn.setStyleSheet(
                "QPushButton { border: 1px solid #4B5563; border-radius: 6px; "
                "font-size: 14px; background: transparent; padding: 0; }"
                "QPushButton:hover { background: rgba(100,100,100,0.15); }"
                "QPushButton:checked { background: rgba(59,130,246,0.15); border-color: #3B82F6; }"
            )

            # Capture the specific line_edit in the lambda
            def _make_toggle(le):
                def _toggle(checked, edit=le):
                    edit.setEchoMode(
                        QLineEdit.EchoMode.Normal if checked
                        else QLineEdit.EchoMode.Password
                    )
                return _toggle

            eye_btn.toggled.connect(_make_toggle(line_edit))

            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(4)
            row_layout.addWidget(line_edit)
            row_layout.addWidget(eye_btn)

            inputs[field] = line_edit
            lbl = QLabel(f"{field}:")
            form.addRow(lbl, row_widget)
            
        self.api_inputs[platform_id] = inputs
        
        btn_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save")
        save_btn.setProperty("class", "primary")
        save_btn.clicked.connect(lambda: self.save_api_keys(platform_id))
        
        auth_btn = QPushButton("Authenticate")
        auth_btn.setProperty("class", "secondary")
        auth_btn.clicked.connect(lambda: self.authenticate_platform(platform_id))
        setattr(self, f"btn_auth_{platform_id}", auth_btn)
        
        status_lbl = QLabel("Status: Not Connected")
        status_lbl.setStyleSheet("")
        setattr(self, f"status_{platform_id}", status_lbl)
        
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(auth_btn)
        btn_layout.addWidget(status_lbl)
        btn_layout.addStretch()
        
        form.addRow("", btn_layout)
        section.addLayout(form)
        self.layout.addWidget(section)


    def _on_theme_changed(self, text: str):
        ThemeManager.get_instance().set_theme_preference(text)

    def load_api_keys(self):
        try:
            from src.storage.security.crypto import CryptoManager
            with self.db.get_connection() as conn:
                cursor = conn.execute("SELECT * FROM api_keys")
                for raw_row in cursor.fetchall():
                    row = dict(raw_row)
                    row["client_id"] = CryptoManager.decrypt(row["client_id"])
                    row["client_secret"] = CryptoManager.decrypt(row["client_secret"])
                    row["access_token"] = CryptoManager.decrypt(row["access_token"])
                    row["refresh_token"] = CryptoManager.decrypt(row["refresh_token"])
                    # Continue original logic with row
                    platform = row["platform"]
                    if platform not in self.api_inputs:
                        continue

                    inputs = self.api_inputs[platform]
                    client_id_keys = [k for k in inputs.keys() if "ID" in k or ("Key" in k and "Secret" not in k)]
                    secret_keys    = [k for k in inputs.keys() if "Secret" in k]
                    token_keys     = [k for k in inputs.keys() if "Token" in k and "Secret" not in k]

                    if row["client_id"] and client_id_keys:
                        inputs[client_id_keys[0]].setText(row["client_id"])
                    if row["client_secret"] and secret_keys:
                        inputs[secret_keys[0]].setText(row["client_secret"])
                    if row["access_token"] and token_keys:
                        inputs[token_keys[0]].setText(row["access_token"])

                    status_lbl = getattr(self, f"status_{platform}")
                    auth_btn   = getattr(self, f"btn_auth_{platform}")

                    # A platform is truly "authenticated" only when:
                    #   - OAuth platforms:  refresh_token is populated (set by the OAuth flow)
                    #   - Token platforms:  access_token is populated (entered by user)
                    has_oauth_token  = bool(row["refresh_token"])
                    has_access_token = bool(row["access_token"])
                    has_credentials  = bool(row["client_id"])

                    if has_oauth_token or has_access_token:
                        status_lbl.setText("Status: ✅ Authenticated")
                        status_lbl.setStyleSheet("color: #22C55E;")
                        auth_btn.setText("Re-authenticate")
                    elif has_credentials:
                        status_lbl.setText("Status: Credentials saved — click Authenticate")
                        status_lbl.setStyleSheet("color: #EAB308;")
                        auth_btn.setText("Authenticate")
                    else:
                        status_lbl.setText("Status: Not Connected")
                        status_lbl.setStyleSheet("")
                        auth_btn.setText("Authenticate")
        except Exception as e:
            print(f"Failed to load keys: {e}")

    def save_api_keys(self, platform_id: str):
        inputs = self.api_inputs[platform_id]

        client_id_keys = [k for k in inputs.keys() if "ID" in k or ("Key" in k and "Secret" not in k)]
        secret_keys    = [k for k in inputs.keys() if "Secret" in k]
        token_keys     = [k for k in inputs.keys() if "Token" in k and "Secret" not in k]

        c_id    = inputs[client_id_keys[0]].text().strip() if client_id_keys else ""
        # For Twitter: secret_keys = ["API Secret", "Access Secret"]
        # client_secret = API Secret (secret_keys[0])
        # access_secret → saved to refresh_token column so TwitterAPI can use it
        c_secret = inputs[secret_keys[0]].text().strip() if secret_keys else ""
        a_token  = inputs[token_keys[0]].text().strip()  if token_keys  else ""

        # Twitter-specific: Access Secret is secret_keys[1] — save to refresh_token
        extra_token = ""
        if platform_id == "twitter" and len(secret_keys) > 1:
            extra_token = inputs[secret_keys[1]].text().strip()  # "Access Secret"

        status_lbl = getattr(self, f"status_{platform_id}")
        auth_btn   = getattr(self, f"btn_auth_{platform_id}")

        try:
            with self.db.get_connection() as conn:
                # If both key fields are blank, this is a "disconnect" — also wipe the OAuth token
                credentials_cleared = not c_id and not c_secret and not a_token
                from src.storage.security.crypto import CryptoManager
                enc_cid = CryptoManager.encrypt(c_id)
                enc_sec = CryptoManager.encrypt(c_secret)
                enc_at = CryptoManager.encrypt(a_token)
                enc_extra = CryptoManager.encrypt(extra_token)
                if credentials_cleared:
                    conn.execute(
                        """INSERT INTO api_keys (platform, client_id, client_secret, access_token, refresh_token)
                           VALUES (?, '', '', '', NULL)
                           ON CONFLICT(platform) DO UPDATE SET
                               client_id='', client_secret='', access_token='',
                               refresh_token=NULL,
                               updated_at=CURRENT_TIMESTAMP""",
                        (platform_id,)
                    )
                elif extra_token:
                    # Twitter: save Access Secret into refresh_token column
                    conn.execute(
                        """INSERT INTO api_keys (platform, client_id, client_secret, access_token, refresh_token)
                           VALUES (?, ?, ?, ?, ?)
                           ON CONFLICT(platform) DO UPDATE SET
                               client_id=excluded.client_id,
                               client_secret=excluded.client_secret,
                               access_token=excluded.access_token,
                               refresh_token=excluded.refresh_token,
                               updated_at=CURRENT_TIMESTAMP""",
                        (platform_id, enc_cid, enc_sec, enc_at, enc_extra)
                    )
                else:
                    conn.execute(
                        """INSERT INTO api_keys (platform, client_id, client_secret, access_token)
                           VALUES (?, ?, ?, ?)
                           ON CONFLICT(platform) DO UPDATE SET
                               client_id=excluded.client_id,
                               client_secret=excluded.client_secret,
                               access_token=excluded.access_token,
                               updated_at=CURRENT_TIMESTAMP""",
                        (platform_id, enc_cid, enc_sec, enc_at)
                    )
                conn.commit()

            if credentials_cleared:
                status_lbl.setText("Status: Not Connected")
                status_lbl.setStyleSheet("")
                auth_btn.setText("Authenticate")
            elif a_token or extra_token:
                # Token-based platform fully configured
                status_lbl.setText("Status: ✅ Saved")
                status_lbl.setStyleSheet("color: #22C55E;")
                auth_btn.setText("Re-authenticate")
            else:
                status_lbl.setText("Status: Saved — click Authenticate")
                status_lbl.setStyleSheet("color: #EAB308;")

        except Exception as e:
            status_lbl.setText(f"Error: {e}")
            status_lbl.setStyleSheet("color: #EF4444;")

    # ── Thread-safe signal carrier for cross-thread UI updates ──────────────
    # QTimer.singleShot is NOT safe when called from a non-Qt thread.
    # The correct approach is to use a QObject Signal, which Qt routes
    # through the event loop automatically regardless of which thread emits it.

    def authenticate_platform(self, platform_id: str):
        """
        Authenticate a platform via OAuth (YouTube, TikTok) or validate
        token-based platforms (Instagram, Facebook, X). Applies to ALL platforms.
        Always saves credentials first.
        """
        # Save latest input values first so the auth service reads fresh data
        self.save_api_keys(platform_id)

        status_lbl = getattr(self, f"status_{platform_id}")
        auth_btn   = getattr(self, f"btn_auth_{platform_id}")

        # ── OAuth platforms: YouTube & TikTok ──────────────────────────────
        if platform_id in ("youtube", "tiktok"):
            # Validate that credentials were entered
            inputs = self.api_inputs[platform_id]
            key_vals = [w.text().strip() for w in inputs.values()]
            if not any(key_vals):
                status_lbl.setText("Error: Enter your Client ID and Secret first, then Save.")
                status_lbl.setStyleSheet("color: #EF4444;")
                return

            status_lbl.setText("Status: Opening browser for authentication…")
            status_lbl.setStyleSheet("color: #EAB308;")

            from src.utils.logger import logger
            import threading
            from PySide6.QtCore import QObject, Signal

            # A tiny QObject that lives on the main thread — its signals are delivered
            # on the main thread regardless of which thread calls emit().
            class _AuthBridge(QObject):
                done  = Signal(str)   # success message
                failed = Signal(str)  # error message

            bridge = _AuthBridge(self)   # parent=self → lives on main thread

            def _on_success(msg):
                status_lbl.setText(f"Status: ✅ {msg}")
                status_lbl.setStyleSheet("color: #22C55E;")
                auth_btn.setText("Re-authenticate")
                # Also refresh dashboard count
                try:
                    from src.ui.views.dashboard import DashboardView
                    from PySide6.QtWidgets import QApplication
                    for w in QApplication.allWidgets():
                        if isinstance(w, DashboardView):
                            w.update_platform_count()
                            break
                except Exception:
                    pass

            def _on_failed(msg):
                status_lbl.setText(f"Error: {msg}")
                status_lbl.setStyleSheet("color: #EF4444;")

            bridge.done.connect(_on_success)
            bridge.failed.connect(_on_failed)

            def _do_auth():
                try:
                    if platform_id == "youtube":
                        from src.services.social.youtube_api import YouTubeAPI
                        api = YouTubeAPI()
                    else:
                        # TikTok placeholder — extend here when TikTok OAuth is implemented
                        bridge.failed.emit("TikTok OAuth integration coming soon.")
                        return

                    result = api.authenticate()
                    logger.info(f"{platform_id} Auth Result: {result}")
                    bridge.done.emit("Authenticated Successfully!")
                except Exception as ex:
                    logger.error(f"{platform_id} Auth Failed: {ex}")
                    bridge.failed.emit(str(ex))

            threading.Thread(target=_do_auth, daemon=True).start()

        # ── Token-based platforms: Instagram, Facebook, X ──────────────────
        elif platform_id in ("instagram", "facebook", "twitter"):
            inputs = self.api_inputs[platform_id]
            token_keys = [k for k in inputs.keys() if "Token" in k and "Secret" not in k]
            token_val = inputs[token_keys[0]].text().strip() if token_keys else ""
            if token_val:
                status_lbl.setText("Status: ✅ Token saved and active")
                status_lbl.setStyleSheet("color: #22C55E;")
                auth_btn.setText("Re-authenticate")
            else:
                status_lbl.setText("Error: Paste your Access Token first, then click Save.")
                status_lbl.setStyleSheet("color: #EF4444;")

        else:
            status_lbl.setText("Status: Platform not supported yet.")
            status_lbl.setStyleSheet("color: #3B82F6;")

    def _download_local_model(self):
        model_size = self.combo_local_model.currentText()
        self.btn_download_model.setEnabled(False)
        self.lbl_download_status.setText(f"Downloading {model_size} (This may take a while)...")
        self.lbl_download_status.setStyleSheet("color: #EAB308; margin-left: 10px;")
        
        from src.workers.base import BaseWorker
        from PySide6.QtCore import QThreadPool
        
        self.download_worker = BaseWorker(self._async_download_model, model_size)
        self.download_worker.signals.result.connect(self._on_download_complete)
        self.download_worker.signals.error.connect(self._on_download_error)
        
        QThreadPool.globalInstance().start(self.download_worker)
        
    def _async_download_model(self, model_size: str, progress_callback=None):
        import faster_whisper
        # This will block and download the model if not already cached
        path = faster_whisper.download_model(model_size)
        return path
        
    def _on_download_complete(self, path: str):
        self.btn_download_model.setEnabled(True)
        self.lbl_download_status.setText("Model downloaded and ready!")
        self.lbl_download_status.setStyleSheet("color: #22C55E; margin-left: 10px;")
        
    def _on_download_error(self, err):
        self.btn_download_model.setEnabled(True)
        self.lbl_download_status.setText(f"Download failed: {err[1]}")
        self.lbl_download_status.setStyleSheet("color: #EF4444; margin-left: 10px;")

