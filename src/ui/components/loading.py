from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt

class LoadingComponent(QWidget):
    """
    Reusable loading component with progress bar.
    """
    def __init__(self, message: str = "Loading..."):
        super().__init__()
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.lbl_message = QLabel(message)
        self.lbl_message.setProperty("class", "subtitle")
        self.lbl_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_message)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indeterminate by default
        self.progress_bar.setFixedWidth(300)
        layout.addWidget(self.progress_bar)
        
        self.setLayout(layout)

    def set_message(self, message: str):
        self.lbl_message.setText(message)

    def set_progress(self, value: int, maximum: int = 100):
        self.progress_bar.setRange(0, maximum)
        self.progress_bar.setValue(value)
        
    def set_indeterminate(self):
        self.progress_bar.setRange(0, 0)
