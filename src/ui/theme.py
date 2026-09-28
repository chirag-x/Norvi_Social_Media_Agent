from PySide6.QtCore import QObject, Signal, QSettings, Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QApplication

class ThemeManager(QObject):
    theme_changed = Signal(dict)
    
    DARK_COLORS = {
        "bg_main": "#090B10",
        "bg_secondary": "#11151D",
        "bg_tertiary": "#171C26",
        "text_main": "#F5F7FA",
        "text_secondary": "#A8B0BD",
        "text_muted": "#70798A",
        "primary": "#3578FF",
        "primary_hover": "#52A0FF",
        "danger": "#FF5252",
        "border": "#171C26"
    }
    
    LIGHT_COLORS = {
        "bg_main": "#F5F7FA",
        "bg_secondary": "#FFFFFF",
        "bg_tertiary": "#E5E7EB",
        "text_main": "#11151D",
        "text_secondary": "#4B5563",
        "text_muted": "#9CA3AF",
        "primary": "#3578FF",
        "primary_hover": "#52A0FF",
        "danger": "#FF5252",
        "border": "#E5E7EB"
    }

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ThemeManager()
        return cls._instance

    def __init__(self):
        super().__init__()
        self.settings = QSettings("Norvi", "SocialMediaAgent")
        
        # Listen to system theme changes
        hints = QGuiApplication.styleHints()
        hints.colorSchemeChanged.connect(self._on_system_theme_changed)

    def set_theme_preference(self, preference: str):
        # preference: "System", "Dark", "Light"
        self.settings.setValue("theme_preference", preference)
        self.apply_theme()

    def get_theme_preference(self) -> str:
        return self.settings.value("theme_preference", "System")

    def get_active_colors(self) -> dict:
        pref = self.get_theme_preference()
        if pref == "Dark":
            return self.DARK_COLORS
        elif pref == "Light":
            return self.LIGHT_COLORS
        else: # System
            scheme = QGuiApplication.styleHints().colorScheme()
            if scheme == Qt.ColorScheme.Dark:
                return self.DARK_COLORS
            else:
                return self.LIGHT_COLORS

    def apply_theme(self):
        c = self.get_active_colors()
        qss = f"""
        QMainWindow {{ background-color: {c['bg_main']}; }}
        QWidget#content_stack {{ background-color: {c['bg_main']}; }}
        QWidget#sidebar {{ background-color: {c['bg_secondary']}; color: {c['text_main']}; }}
        
        QLabel {{ color: {c['text_main']}; }}
        QLabel[class="title"] {{ font-size: 24px; font-weight: bold; margin-bottom: 20px; }}
        QLabel[class="sidebar_title"] {{ font-size: 18px; font-weight: bold; margin: 10px 0px 20px 0px; }}
        QLabel[class="subtitle"] {{ color: {c['text_secondary']}; font-size: 14px; }}
        QLabel[class="error"] {{ color: {c['danger']}; font-size: 12px; margin-top: 5px; }}
        QLabel[class="error_title"] {{ color: {c['danger']}; font-size: 20px; font-weight: bold; margin-bottom: 10px; }}
        
        QPushButton[class="nav"] {{ background-color: transparent; text-align: left; padding: 10px; border-radius: 5px; font-size: 14px; color: {c['text_main']}; }}
        QPushButton[class="nav"]:hover {{ background-color: {c['bg_tertiary']}; }}
        QPushButton[class="nav_logout"] {{ background-color: transparent; text-align: left; padding: 10px; border-radius: 5px; font-size: 14px; color: {c['danger']}; }}
        QPushButton[class="nav_logout"]:hover {{ background-color: {c['bg_tertiary']}; }}
        
        QPushButton[class="primary"] {{ background-color: {c['primary']}; color: white; padding: 10px; border-radius: 5px; font-weight: bold; font-size: 16px; margin-top: 15px; }}
        QPushButton[class="primary"]:hover {{ background-color: {c['primary_hover']}; }}
        QPushButton[class="primary"]:disabled {{ background-color: {c['text_muted']}; }}
        
        QFrame#login_container {{ background-color: {c['bg_secondary']}; border-radius: 10px; padding: 20px; }}
        
        QLineEdit {{ background-color: {c['bg_tertiary']}; color: {c['text_main']}; border: 1px solid {c['text_muted']}; border-radius: 5px; padding: 10px; font-size: 14px; margin-bottom: 10px; }}
        QLineEdit:focus {{ border: 1px solid {c['primary']}; }}
        
        QProgressBar {{ border: 1px solid {c['bg_tertiary']}; border-radius: 5px; background-color: {c['bg_secondary']}; height: 10px; }}
        QProgressBar::chunk {{ background-color: {c['primary']}; border-radius: 5px; }}
        
        QComboBox {{ background-color: {c['bg_tertiary']}; color: {c['text_main']}; border: 1px solid {c['text_muted']}; border-radius: 5px; padding: 5px; }}
        QComboBox:drop-down {{ border: none; }}
        QComboBox QAbstractItemView {{ background-color: {c['bg_secondary']}; color: {c['text_main']}; selection-background-color: {c['bg_tertiary']}; }}
        """
        app = QApplication.instance()
        if app:
            app.setStyleSheet(qss)
        self.theme_changed.emit(c)
        
    def _on_system_theme_changed(self, scheme):
        if self.get_theme_preference() == "System":
            self.apply_theme()
