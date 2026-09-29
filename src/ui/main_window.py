from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget, QLabel, QSizePolicy
from PySide6.QtGui import QIcon, QKeySequence, QShortcut
from PySide6.QtCore import QSettings, Qt

from src.ui.components.sidebar import Sidebar
from src.ui.views.dashboard import DashboardView
from src.ui.views.settings import SettingsView
from src.ui.views.placeholder import PlaceholderView


def _apply_dwm_dark_titlebar(hwnd: int, dark: bool = True):
    """
    Use the Windows DWM API to make the native title bar dark (or light).
    Works on Windows 10 1903+ for dark mode. Windows 11 22000+ also accepts
    DWMWA_CAPTION_COLOR (35) and DWMWA_TEXT_COLOR (36).
    Silently ignored on non-Windows platforms.
    """
    try:
        import ctypes
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        value = ctypes.c_int(1 if dark else 0)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE,
            ctypes.byref(value), ctypes.sizeof(value)
        )
        # Windows 11: set exact caption + text colour
        DWMWA_CAPTION_COLOR = 35
        DWMWA_TEXT_COLOR    = 36
        # COLORREF is 0x00BBGGRR
        if dark:
            caption = ctypes.c_uint(0x00170D0D)   # very dark navy — matches #0D1117
            text    = ctypes.c_uint(0x00F9F5F1)   # near-white  — matches #F1F5F9
        else:
            caption = ctypes.c_uint(0x00F9F9F9)   # near-white
            text    = ctypes.c_uint(0x001A1A1A)   # near-black
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, DWMWA_CAPTION_COLOR,
            ctypes.byref(caption), ctypes.sizeof(caption)
        )
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, DWMWA_TEXT_COLOR,
            ctypes.byref(text), ctypes.sizeof(text)
        )
    except Exception:
        pass  # Non-Windows or older Windows — safe to ignore


class MainWindow(QMainWindow):
    """
    The main application window holding the sidebar and the main content area.
    Uses the native Windows title bar (enabling Snap, F11, taskbar features)
    styled via DWM APIs.
    """
    def __init__(self):
        super().__init__()

        from PySide6.QtGui import QIcon
        self.setWindowIcon(QIcon("assets/nexus_norvi_agent_logo.jpg"))
        self.setWindowTitle("Nexus")
        self.resize(1200, 800)
        self.setMinimumSize(800, 600)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        from PySide6.QtGui import QGuiApplication
        screen = QGuiApplication.primaryScreen().geometry()
        x = (screen.width() - 1200) // 2
        y = (screen.height() - 800) // 2
        self.move(x, max(0, y))

        # Restore saved geometry
        self.settings = QSettings("Nexus", "SocialMediaAgent")
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
        window_state = self.settings.value("windowState")
        if window_state:
            self.restoreState(window_state)

        # ── Central widget ────────────────────────────────────────────────────
        central_widget = QWidget()
        central_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ── Sidebar ───────────────────────────────────────────────────────────
        self.sidebar = Sidebar()
        self.sidebar.navigation_requested.connect(self.navigate_to)
        self.sidebar.logout_requested.connect(self.handle_logout)
        self.sidebar.hide()
        main_layout.addWidget(self.sidebar)

        # ── Right side (content + footer) ─────────────────────────────────────
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("content_stack")
        self.content_stack.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        right_layout.addWidget(self.content_stack)

        # Footer
        self.footer = QLabel(
            'Designed and developed by <a href="https://nor-vi.in/contact/" '
            'style="color: #3B82F6; text-decoration: none; font-weight: bold;">Norvi Agency</a>'
        )
        self.footer.setOpenExternalLinks(True)
        self.footer.setStyleSheet("color: #6B7280; font-size: 12px; margin-bottom: 5px; margin-right: 20px;")
        self.footer.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.footer.hide()
        right_layout.addWidget(self.footer)

        main_layout.addLayout(right_layout)

        # ── Keyboard shortcuts (native behaviour) ─────────────────────────────
        # F11 — toggle fullscreen / maximised
        f11 = QShortcut(QKeySequence(Qt.Key.Key_F11), self)
        f11.activated.connect(self._toggle_maximize)

        # Alt+F4 is handled by OS; Ctrl+W close
        ctrl_w = QShortcut(QKeySequence("Ctrl+W"), self)
        ctrl_w.activated.connect(self.close)

        # ── Register Views ────────────────────────────────────────────────────
        from src.ui.views.login import LoginView
        from src.services.auth.session import SessionManager
        from src.ui.views.discover import DiscoverView
        from src.ui.views.clip_lab import ClipLabView
        from src.ui.views.publishing_queue import PublishingQueueView
        from src.ui.views.calendar_view import CalendarView
        from src.ui.views.analytics import AnalyticsView
        from src.ui.views.settings import SettingsView
        from src.ui.views.help import HelpView

        self.login_view = LoginView()
        self.login_view.login_successful.connect(self.handle_login_success)

        self.views = {
            "login":     self.login_view,
            "dashboard": DashboardView(),
            "discover":  DiscoverView(),
            "clip_lab":  ClipLabView(),
            "calendar":  CalendarView(),
            "queue":     PublishingQueueView(),
            "analytics": AnalyticsView(),
            "settings":  SettingsView(),
            "help":      HelpView(),
        }

        for view_widget in self.views.values():
            self.content_stack.addWidget(view_widget)

        if SessionManager.is_authenticated():
            self.handle_login_success()
        else:
            self.navigate_to("login")

    # ── DWM styling ───────────────────────────────────────────────────────────
    def showEvent(self, event):
        """Apply DWM dark title bar once the window handle is available."""
        super().showEvent(event)
        self._refresh_titlebar_color()

    def _refresh_titlebar_color(self):
        """Reads the active theme and styles the native title bar accordingly."""
        try:
            from src.ui.theme import ThemeManager
            dark = ThemeManager.get_instance().is_dark_mode()
        except Exception:
            dark = True
        _apply_dwm_dark_titlebar(int(self.winId()), dark=dark)

    # ── Fullscreen / maximize ─────────────────────────────────────────────────
    def _toggle_maximize(self):
        if self.isMaximized() or self.isFullScreen():
            self.showNormal()
        else:
            self.showMaximized()

    # ── Auth lifecycle ────────────────────────────────────────────────────────
    def handle_login_success(self):
        self.sidebar.show()
        self.footer.show()
        self.navigate_to("dashboard")
        self._refresh_titlebar_color()

        from src.services.social.publishing_daemon import PublishingDaemon
        PublishingDaemon.get_instance().start()

    def handle_logout(self):
        self.sidebar.hide()
        self.footer.hide()

        from src.services.social.publishing_daemon import PublishingDaemon
        PublishingDaemon.get_instance().stop()

        self.navigate_to("login")

    def navigate_to(self, view_name: str):
        if view_name in self.views:
            self.content_stack.setCurrentWidget(self.views[view_name])

    # ── Theme change hook ─────────────────────────────────────────────────────
    def on_theme_changed(self):
        """Call this whenever the user changes the theme to re-colour the title bar."""
        self._refresh_titlebar_color()

    # ── Close ─────────────────────────────────────────────────────────────────
    def closeEvent(self, event):
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())

        from src.ai.ollama_manager import OllamaManager
        OllamaManager.get_instance().stop_safely()

        super().closeEvent(event)
