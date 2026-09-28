from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QHBoxLayout
from PySide6.QtCore import Qt
from src.ui.theme import ThemeManager

class SettingsView(QWidget):
    """
    Settings view for configuring the application.
    """
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        title = QLabel("Settings")
        title.setProperty("class", "title")
        layout.addWidget(title)
        
        # Theme Setting
        theme_layout = QHBoxLayout()
        theme_label = QLabel("Theme Preference:")
        theme_label.setProperty("class", "subtitle")
        theme_layout.addWidget(theme_label)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["System", "Dark", "Light"])
        self.theme_combo.setFixedWidth(150)
        current_pref = ThemeManager.get_instance().get_theme_preference()
        self.theme_combo.setCurrentText(current_pref)
        self.theme_combo.currentTextChanged.connect(self._on_theme_changed)
        theme_layout.addWidget(self.theme_combo)
        
        theme_layout.addStretch()
        layout.addLayout(theme_layout)
        
        info = QLabel("\nMore configuration and preferences will appear here.")
        info.setProperty("class", "subtitle")
        layout.addWidget(info)
        
        layout.addStretch()
        self.setLayout(layout)

    def _on_theme_changed(self, text: str):
        ThemeManager.get_instance().set_theme_preference(text)
