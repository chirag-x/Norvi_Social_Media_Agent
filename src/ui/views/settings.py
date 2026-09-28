from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, 
    QScrollArea, QGroupBox, QLineEdit, QPushButton, QFormLayout
)
from PySide6.QtCore import Qt
from src.ui.theme import ThemeManager
from src.storage.database.database import DatabaseManager

class SettingsView(QWidget):
    """
    Settings view for configuring the application and connecting Social APIs.
    """
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager.get_instance()
        
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        title = QLabel("Settings & Integrations")
        title.setProperty("class", "title")
        main_layout.addWidget(title)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        scroll_content = QWidget()
        self.layout = QVBoxLayout(scroll_content)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Appearance
        self._build_appearance_section()
        
        # Social APIs
        api_title = QLabel("\nSocial Media Developer Accounts (Phase 19)")
        api_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #FFFFFF;")
        self.layout.addWidget(api_title)
        
        self.api_inputs = {}
        
        self._build_api_section("YouTube Data API v3", "youtube", ["Client ID", "Client Secret"])
        self._build_api_section("TikTok for Developers", "tiktok", ["Client Key", "Client Secret"])
        self._build_api_section("Instagram Graph API", "instagram", ["App ID", "App Secret", "Access Token"])
        self._build_api_section("Facebook Graph API", "facebook", ["App ID", "App Secret", "Access Token"])
        self._build_api_section("X (Twitter) API v2", "twitter", ["API Key", "API Secret", "Access Token", "Access Secret"])
        
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
        
        self.load_api_keys()

    def _build_appearance_section(self):
        group = QGroupBox("Appearance")
        group.setStyleSheet("QGroupBox { font-weight: bold; border: 1px solid #374151; border-radius: 6px; margin-top: 10px; } QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; }")
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
        group.setLayout(layout)
        self.layout.addWidget(group)

    def _build_api_section(self, title_text: str, platform_id: str, fields: list):
        group = QGroupBox(title_text)
        group.setStyleSheet("QGroupBox { font-weight: bold; border: 1px solid #374151; border-radius: 6px; margin-top: 10px; padding-top: 15px; }")
        form = QFormLayout()
        
        inputs = {}
        for field in fields:
            line_edit = QLineEdit()
            line_edit.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)
            inputs[field] = line_edit
            form.addRow(f"{field}:", line_edit)
            
        self.api_inputs[platform_id] = inputs
        
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save & Authenticate")
        save_btn.setProperty("class", "btn-primary")
        save_btn.clicked.connect(lambda: self.save_api_keys(platform_id))
        
        status_lbl = QLabel("Status: Not Connected")
        status_lbl.setStyleSheet("color: #9CA3AF;")
        setattr(self, f"status_{platform_id}", status_lbl)
        
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(status_lbl)
        btn_layout.addStretch()
        
        form.addRow("", btn_layout)
        group.setLayout(form)
        self.layout.addWidget(group)

    def _on_theme_changed(self, text: str):
        ThemeManager.get_instance().set_theme_preference(text)

    def load_api_keys(self):
        try:
            with self.db.get_connection() as conn:
                cursor = conn.execute("SELECT * FROM api_keys")
                for row in cursor.fetchall():
                    platform = row["platform"]
                    if platform in self.api_inputs:
                        # Depending on platform, map DB columns back to inputs
                        # This is a simplified loader for the UI
                        inputs = self.api_inputs[platform]
                        
                        client_id_keys = [k for k in inputs.keys() if "ID" in k or "Key" in k and "Secret" not in k]
                        secret_keys = [k for k in inputs.keys() if "Secret" in k]
                        token_keys = [k for k in inputs.keys() if "Token" in k and "Secret" not in k]
                        
                        if row["client_id"] and client_id_keys:
                            inputs[client_id_keys[0]].setText(row["client_id"])
                        if row["client_secret"] and secret_keys:
                            inputs[secret_keys[0]].setText(row["client_secret"])
                        if row["access_token"] and token_keys:
                            inputs[token_keys[0]].setText(row["access_token"])
                            
                        # Update status label
                        if row["client_id"] or row["access_token"]:
                            status_lbl = getattr(self, f"status_{platform}")
                            status_lbl.setText("Status: Configured (Requires Auth)")
                            status_lbl.setStyleSheet("color: #EAB308;") # Yellow
        except Exception as e:
            print(f"Failed to load keys: {e}")

    def save_api_keys(self, platform_id: str):
        inputs = self.api_inputs[platform_id]
        
        client_id_keys = [k for k in inputs.keys() if "ID" in k or "Key" in k and "Secret" not in k]
        secret_keys = [k for k in inputs.keys() if "Secret" in k]
        token_keys = [k for k in inputs.keys() if "Token" in k and "Secret" not in k]
        
        c_id = inputs[client_id_keys[0]].text() if client_id_keys else ""
        c_secret = inputs[secret_keys[0]].text() if secret_keys else ""
        a_token = inputs[token_keys[0]].text() if token_keys else ""
        
        try:
            with self.db.get_connection() as conn:
                conn.execute("""
                    INSERT INTO api_keys (platform, client_id, client_secret, access_token) 
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(platform) DO UPDATE SET 
                        client_id=excluded.client_id,
                        client_secret=excluded.client_secret,
                        access_token=excluded.access_token,
                        updated_at=CURRENT_TIMESTAMP
                """, (platform_id, c_id, c_secret, a_token))
                conn.commit()
                
            status_lbl = getattr(self, f"status_{platform_id}")
            status_lbl.setText("Status: Saved!")
            status_lbl.setStyleSheet("color: #22C55E;")
        except Exception as e:
            status_lbl = getattr(self, f"status_{platform_id}")
            status_lbl.setText(f"Error: {e}")
            status_lbl.setStyleSheet("color: #EF4444;")
