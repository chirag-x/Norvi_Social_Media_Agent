import asyncio
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, 
    QPushButton, QFrame, QHBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from src.services.auth.client import AuthClient
from src.services.auth.session import SessionManager
from src.workers.base import BaseWorker
from PySide6.QtCore import QThreadPool

class LoginView(QWidget):
    """
    Login screen asking for Email, Password, and Activation Key.
    """
    login_successful = Signal()

    def __init__(self):
        super().__init__()
        self.auth_client = AuthClient()
        self.thread_pool = QThreadPool.globalInstance()
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Login Container
        container = QFrame()
        container.setFixedWidth(400)
        container.setObjectName("login_container")
        
        layout = QVBoxLayout(container)
        
        # Title
        title = QLabel("Norvi Agent Login")
        title.setProperty("class", "title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Email Field
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email Address")
        layout.addWidget(self.email_input)
        
        # Password Field
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)
        
        # Activation Key Field
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Activation Key")
        layout.addWidget(self.key_input)
        
        # Error Label
        self.error_label = QLabel("")
        self.error_label.setProperty("class", "error")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.hide()
        layout.addWidget(self.error_label)
        
        # Login Button
        self.login_btn = QPushButton("Login")
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_btn.setProperty("class", "primary")
        self.login_btn.clicked.connect(self.on_login_clicked)
        layout.addWidget(self.login_btn)
        
        main_layout.addWidget(container)

    def on_login_clicked(self):
        email = self.email_input.text().strip()
        password = self.password_input.text()
        activation_key = self.key_input.text().strip()
        
        if not email or not password or not activation_key:
            self.show_error("All fields are required.")
            return
            
        self.error_label.hide()
        self.login_btn.setEnabled(False)
        self.login_btn.setText("Authenticating...")
        
        # Run async login in a background worker
        worker = BaseWorker(self._perform_login_sync, email, password, activation_key)
        worker.signals.result.connect(self.on_login_result)
        worker.signals.error.connect(self.on_login_error)
        self.thread_pool.start(worker)

    def _perform_login_sync(self, email, password, activation_key):
        # We need to run the async httpx call synchronously inside the worker thread
        return asyncio.run(self.auth_client.login(email, password, activation_key))

    def on_login_result(self, result):
        success, message, token = result
        if success and token:
            if SessionManager.save_token(token):
                # Ensure local DB knows about this user
                from src.storage.daos.user_dao import UserDAO
                UserDAO().create_or_update(email)
                
                self.login_successful.emit()
                self.reset()
            else:
                self.show_error("Login succeeded, but failed to save session locally.")
                self.reset_button()
        else:
            self.show_error(message)
            self.reset_button()

    def on_login_error(self, error_tuple):
        self.show_error("An unexpected error occurred during authentication.")
        self.reset_button()

    def show_error(self, message: str):
        self.error_label.setText(message)
        self.error_label.show()
        
    def reset_button(self):
        self.login_btn.setEnabled(True)
        self.login_btn.setText("Login")

    def reset(self):
        """Clears all input fields and resets the login button."""
        self.email_input.clear()
        self.password_input.clear()
        self.key_input.clear()
        self.error_label.hide()
        self.reset_button()
