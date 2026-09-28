from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSettings, QByteArray

from src.ui.components.sidebar import Sidebar
from src.ui.views.dashboard import DashboardView
from src.ui.views.settings import SettingsView
from src.ui.views.placeholder import PlaceholderView

class MainWindow(QMainWindow):
    """
    The main application window holding the sidebar and the main content area.
    """
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Norvi Social Media Agent")
        # Default size, will be overridden by settings if available
        self.resize(1200, 800)
        
        # Center the window on the screen (fallback if no settings)
        from PySide6.QtGui import QGuiApplication
        screen = QGuiApplication.primaryScreen().geometry()
        x = (screen.width() - 1200) // 2
        y = (screen.height() - 800) // 2
        self.move(x, max(0, y))

        # Restore window geometry and state
        self.settings = QSettings("Norvi", "SocialMediaAgent")
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
        window_state = self.settings.value("windowState")
        if window_state:
            self.restoreState(window_state)

        
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar (Hidden initially)
        self.sidebar = Sidebar()
        self.sidebar.navigation_requested.connect(self.navigate_to)
        self.sidebar.logout_requested.connect(self.handle_logout)
        self.sidebar.hide()
        main_layout.addWidget(self.sidebar)
        
        # Content Area (Stacked Widget)
        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("content_stack")
        main_layout.addWidget(self.content_stack)
        
        # Import login and session manager
        from src.ui.views.login import LoginView
        from src.services.auth.session import SessionManager
        
        self.login_view = LoginView()
        self.login_view.login_successful.connect(self.handle_login_success)
        
        # Register Views
        from src.ui.views.discover import DiscoverView
        from src.ui.views.clip_lab import ClipLabView
        from src.ui.views.publishing_queue import PublishingQueueView
        from src.ui.views.calendar_view import CalendarView
        from src.ui.views.analytics import AnalyticsView
        
        self.views = {
            "login": self.login_view,
            "dashboard": DashboardView(),
            "discover": DiscoverView(),
            "clip_lab": ClipLabView(),
            "calendar": CalendarView(),
            "queue": PublishingQueueView(),
            "analytics": AnalyticsView(),
            "settings": SettingsView()
        }
        
        # Add views to stack
        for view_widget in self.views.values():
            self.content_stack.addWidget(view_widget)
            
        # Check authentication state
        if SessionManager.is_authenticated():
            self.handle_login_success()
        else:
            self.navigate_to("login")

    def handle_login_success(self):
        """Called when login is successful or token already exists."""
        self.sidebar.show()
        self.navigate_to("dashboard")

    def handle_logout(self):
        """Called when user logs out."""
        self.sidebar.hide()
        self.navigate_to("login")

    def navigate_to(self, view_name: str):
        """Switch the central stacked widget to the requested view."""
        if view_name in self.views:
            self.content_stack.setCurrentWidget(self.views[view_name])

    def closeEvent(self, event):
        """Save window state before closing and shut down background processes."""
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        
        # Shutdown Ollama if we own the process
        from src.ai.ollama_manager import OllamaManager
        OllamaManager.get_instance().stop_safely()
        
        super().closeEvent(event)
