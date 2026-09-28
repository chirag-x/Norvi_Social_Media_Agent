from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Signal, Qt

class Sidebar(QWidget):
    """
    Sidebar component for main navigation.
    Emits navigation_requested(view_name) when a button is clicked.
    """
    navigation_requested = Signal(str)
    logout_requested = Signal()

    def __init__(self):
        super().__init__()
        self.setFixedWidth(200)
        self.setObjectName("sidebar")
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Logo or Title
        title = QLabel("Norvi Agent")
        title.setProperty("class", "sidebar_title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Navigation Buttons
        self.btn_dashboard = self._create_nav_button("Dashboard", "dashboard")
        self.btn_discover = self._create_nav_button("Discover", "discover")
        self.btn_clip_lab = self._create_nav_button("Clip Lab", "clip_lab")
        self.btn_calendar = self._create_nav_button("Calendar", "calendar")
        self.btn_queue = self._create_nav_button("Publishing Queue", "queue")
        self.btn_analytics = self._create_nav_button("Analytics", "analytics")
        
        layout.addWidget(self.btn_dashboard)
        layout.addWidget(self.btn_discover)
        layout.addWidget(self.btn_clip_lab)
        layout.addWidget(self.btn_calendar)
        layout.addWidget(self.btn_queue)
        layout.addWidget(self.btn_analytics)
        
        layout.addStretch()
        
        self.btn_settings = self._create_nav_button("Settings", "settings")
        layout.addWidget(self.btn_settings)
        
        # Logout button
        self.btn_logout = QPushButton("Logout")
        self.btn_logout.setProperty("class", "nav_logout")
        self.btn_logout.clicked.connect(self._handle_logout)
        layout.addWidget(self.btn_logout)
        
        self.setLayout(layout)

    def _handle_logout(self):
        from src.services.auth.session import SessionManager
        SessionManager.clear_session()
        self.logout_requested.emit()

    def _create_nav_button(self, text: str, view_name: str) -> QPushButton:
        btn = QPushButton(text)
        btn.setProperty("class", "nav")
        btn.clicked.connect(lambda: self.navigation_requested.emit(view_name))
        return btn
