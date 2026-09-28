from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Signal, Qt

class ErrorComponent(QWidget):
    """
    Reusable error display component.
    """
    retry_requested = Signal()

    def __init__(self, title: str = "An error occurred", details: str = "", show_retry: bool = True):
        super().__init__()
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.lbl_title = QLabel(title)
        self.lbl_title.setProperty("class", "error_title")
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_title)
        
        self.lbl_details = QLabel(details)
        self.lbl_details.setProperty("class", "subtitle")
        self.lbl_details.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_details)
        
        if show_retry:
            self.btn_retry = QPushButton("Retry")
            self.btn_retry.setFixedWidth(150)
            self.btn_retry.setProperty("class", "primary")
            self.btn_retry.clicked.connect(self.retry_requested.emit)
            layout.addWidget(self.btn_retry, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(layout)
