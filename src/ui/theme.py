from PySide6.QtCore import QObject, Signal, QSettings, Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QApplication

class ThemeManager(QObject):
    theme_changed = Signal(dict)
    
    DARK_COLORS = {
        "bg_main": "#0B0F19",
        "bg_secondary": "#111827",
        "bg_tertiary": "#1F2937",
        "text_main": "#F9FAFB",
        "text_secondary": "#9CA3AF",
        "text_muted": "#6B7280",
        "primary": "#3B82F6",
        "primary_hover": "#2563EB",
        "danger": "#EF4444",
        "border": "#374151"
    }
    
    LIGHT_COLORS = {
        "bg_main": "#F3F4F6",
        "bg_secondary": "#FFFFFF",
        "bg_tertiary": "#E5E7EB",
        "text_main": "#111827",
        "text_secondary": "#4B5563",
        "text_muted": "#9CA3AF",
        "primary": "#3B82F6",
        "primary_hover": "#2563EB",
        "danger": "#EF4444",
        "border": "#D1D5DB"
    }

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ThemeManager()
        return cls._instance

    def __init__(self):
        super().__init__()
        self.settings = QSettings("Nexus", "SocialMediaAgent")
        
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

    def is_dark_mode(self) -> bool:
        return self.get_active_colors() is self.DARK_COLORS

    def apply_theme(self):
        c = self.get_active_colors()
        qss = f"""
        QWidget {{ color: {c['text_main']}; font-family: 'Segoe UI', system-ui, sans-serif; }}
        QMainWindow {{ background-color: {c['bg_main']}; }}
        QWidget#content_stack {{ background-color: {c['bg_main']}; }}
        QWidget#sidebar {{ background-color: {c['bg_secondary']}; border-right: 1px solid {c['border']}; }}
        
        QScrollArea {{ background-color: transparent; border: none; }}
        QScrollArea > QWidget > QWidget {{ background-color: transparent; }}
        
        QLabel[class="title"] {{ font-size: 28px; font-weight: 800; margin-bottom: 16px; letter-spacing: -0.5px; }}
        QLabel[class="sidebar_title"] {{ font-size: 20px; font-weight: 800; margin: 15px 0px 25px 0px; letter-spacing: -0.5px; }}
        QLabel[class="subtitle"] {{ color: {c['text_secondary']}; font-size: 15px; margin-bottom: 20px; }}
        QLabel[class="error"] {{ color: {c['danger']}; font-size: 13px; margin-top: 6px; font-weight: 500; }}
        QLabel[class="error_title"] {{ color: {c['danger']}; font-size: 20px; font-weight: bold; margin-bottom: 10px; }}
        
        QPushButton[class="nav"] {{ background-color: transparent; text-align: left; padding: 12px 16px; border-radius: 8px; font-size: 15px; color: {c['text_secondary']}; font-weight: 600; margin-bottom: 4px; }}
        QPushButton[class="nav"]:hover {{ background-color: {c['bg_tertiary']}; color: {c['text_main']}; }}
        QPushButton[class="nav"]:checked {{ background-color: {c['bg_tertiary']}; color: {c['primary']}; }}
        
        QPushButton[class="nav_logout"] {{ background-color: transparent; text-align: left; padding: 12px 16px; border-radius: 8px; font-size: 15px; color: {c['danger']}; font-weight: 600; }}
        QPushButton[class="nav_logout"]:hover {{ background-color: rgba(239, 68, 68, 0.1); }}
        
        QPushButton[class="primary"] {{ background-color: {c['primary']}; color: white; padding: 12px 24px; border-radius: 8px; font-weight: bold; font-size: 15px; }}
        QPushButton[class="primary"]:hover {{ background-color: {c['primary_hover']}; }}
        QPushButton[class="primary"]:disabled {{ background-color: {c['border']}; color: {c['text_muted']}; }}
        
        QPushButton[class="secondary"] {{ background-color: {c['bg_tertiary']}; color: {c['text_main']}; padding: 12px 24px; border-radius: 8px; font-weight: bold; font-size: 15px; border: 1px solid {c['border']}; }}
        QPushButton[class="secondary"]:hover {{ background-color: {c['bg_secondary']}; border: 1px solid {c['primary']}; }}
        QPushButton[class="secondary"]:disabled {{ background-color: {c['border']}; color: {c['text_muted']}; border: none; }}
        
        QPushButton[class="collapsible_btn"] {{ background-color: {c['bg_secondary']}; color: {c['text_main']}; border: 1px solid {c['border']}; }}
        QPushButton[class="collapsible_btn"]:hover {{ background-color: {c['bg_tertiary']}; }}
        
        QFrame[class="collapsible_content"] {{ background-color: {c['bg_main']}; border: 1px solid {c['border']}; }}
        
        QPushButton[class="duration_btn"] {{ background-color: {c['bg_tertiary']}; color: {c['text_secondary']}; border: 1px solid {c['border']}; border-radius: 6px; font-size: 13px; font-weight: 600; }}
        QPushButton[class="duration_btn"]:hover {{ background-color: {c['bg_secondary']}; color: {c['text_main']}; border: 1px solid {c['primary']}; }}
        QPushButton[class="duration_btn"]:checked {{ background-color: {c['primary']}; color: white; border: 1px solid {c['primary']}; }}
        
        QFrame#login_container, QFrame#card {{ background-color: {c['bg_secondary']}; border-radius: 12px; border: 1px solid {c['border']}; padding: 24px; }}
        
        QLineEdit, QTextEdit, QPlainTextEdit {{ background-color: {c['bg_main']}; color: {c['text_main']}; border: 1px solid {c['border']}; border-radius: 8px; padding: 12px; font-size: 14px; selection-background-color: {c['primary']}; }}
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{ border: 1px solid {c['primary']}; background-color: {c['bg_secondary']}; }}
        
        QProgressBar {{ border: 1px solid {c['border']}; border-radius: 6px; background-color: {c['bg_main']}; height: 12px; text-align: center; color: transparent; }}
        QProgressBar::chunk {{ background-color: {c['primary']}; border-radius: 5px; }}
        
        QComboBox {{ background-color: {c['bg_main']}; color: {c['text_main']}; border: 1px solid {c['border']}; border-radius: 8px; padding: 10px 12px; font-size: 14px; }}
        QComboBox::drop-down {{ border: none; width: 30px; }}
        QComboBox::down-arrow {{ image: none; border-left: 5px solid transparent; border-right: 5px solid transparent; border-top: 5px solid {c['text_muted']}; margin-right: 10px; }}
        QComboBox QAbstractItemView {{ background-color: {c['bg_secondary']}; color: {c['text_main']}; border: 1px solid {c['border']}; border-radius: 8px; selection-background-color: {c['bg_tertiary']}; padding: 4px; outline: 0px; }}
        
        QCheckBox {{ color: {c['text_main']}; font-size: 14px; spacing: 10px; }}
        QCheckBox::indicator {{ width: 20px; height: 20px; border-radius: 6px; border: 1px solid {c['border']}; background-color: {c['bg_main']}; }}
        QCheckBox::indicator:hover {{ border: 1px solid {c['primary']}; }}
        QCheckBox::indicator:checked {{ background-color: {c['primary']}; border: 1px solid {c['primary']}; image: url(none); }}
        
        QListWidget, QTableWidget {{ background-color: {c['bg_secondary']}; border: 1px solid {c['border']}; border-radius: 12px; outline: 0; }}
        QListWidget::item {{ border-bottom: 1px solid {c['border']}; }}
        QTableWidget::item {{ padding: 12px; border-bottom: 1px solid {c['border']}; }}
        QListWidget::item:selected, QTableWidget::item:selected {{ background-color: {c['bg_tertiary']}; color: {c['primary']}; }}
        QHeaderView::section {{ background-color: {c['bg_tertiary']}; color: {c['text_secondary']}; padding: 10px; border: none; font-weight: bold; text-transform: uppercase; font-size: 12px; }}
        
        /* Premium Scrollbars */
        QScrollBar:vertical {{ border: none; background: transparent; width: 10px; margin: 0px; }}
        QScrollBar::handle:vertical {{ background: {c['border']}; min-height: 30px; border-radius: 5px; }}
        QScrollBar::handle:vertical:hover {{ background: {c['text_muted']}; }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ border: none; background: none; }}
        
        QScrollBar:horizontal {{ border: none; background: transparent; height: 10px; margin: 0px; }}
        QScrollBar::handle:horizontal {{ background: {c['border']}; min-width: 30px; border-radius: 5px; }}
        QScrollBar::handle:horizontal:hover {{ background: {c['text_muted']}; }}
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ border: none; background: none; }}
        
        /* QDateTimeEdit & QCalendarWidget — theme-aware */
        QDateTimeEdit {{
            background-color: {c['bg_main']};
            color: {c['text_main']};
            border: 1px solid {c['border']};
            border-radius: 6px;
            padding: 6px 10px;
            font-size: 13px;
        }}
        QDateTimeEdit::drop-down {{ border: none; width: 24px; }}
        QDateTimeEdit::down-arrow {{
            image: none;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 5px solid {c['text_muted']};
            margin-right: 6px;
        }}
        
        /* Calendar popup widget */
        QCalendarWidget QWidget {{
            background-color: {c['bg_secondary']};
            color: {c['text_main']};
            alternate-background-color: {c['bg_tertiary']};
        }}
        QCalendarWidget QAbstractItemView {{
            background-color: {c['bg_secondary']};
            color: {c['text_main']};
            selection-background-color: {c['primary']};
            selection-color: white;
            gridline-color: {c['border']};
        }}
        QCalendarWidget QAbstractItemView:disabled {{ color: {c['text_muted']}; }}
        QCalendarWidget QToolButton {{
            background-color: {c['bg_tertiary']};
            color: {c['text_main']};
            border: none;
            border-radius: 4px;
            padding: 4px 8px;
            font-weight: bold;
        }}
        QCalendarWidget QToolButton:hover {{ background-color: {c['primary']}; color: white; }}
        QCalendarWidget #qt_calendar_navigationbar {{
            background-color: {c['bg_tertiary']};
            padding: 4px;
            border-bottom: 1px solid {c['border']};
        }}
        QCalendarWidget QSpinBox {{
            background-color: {c['bg_main']};
            color: {c['text_main']};
            border: 1px solid {c['border']};
            border-radius: 4px;
            padding: 2px 6px;
        }}
        """
        app = QApplication.instance()
        if app:
            app.setStyleSheet(qss)
        self.theme_changed.emit(c)
        
    def _on_system_theme_changed(self, scheme):
        if self.get_theme_preference() == "System":
            self.apply_theme()
