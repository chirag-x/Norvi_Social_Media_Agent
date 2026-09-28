from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class PlaceholderView(QWidget):
    """
    A temporary placeholder for views that have not been implemented yet.
    """
    def __init__(self, name: str):
        super().__init__()
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel(f"{name} View")
        title.setProperty("class", "title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("This module is under construction.")
        subtitle.setProperty("class", "subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        self.setLayout(layout)
