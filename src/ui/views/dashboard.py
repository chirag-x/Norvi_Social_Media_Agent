from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class DashboardView(QWidget):
    """
    Dashboard view showing application overview.
    """
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        title = QLabel("Dashboard")
        title.setProperty("class", "title")
        layout.addWidget(title)
        
        subtitle = QLabel("Welcome to Norvi Social Media Agent.\nSelect an option from the sidebar to begin.")
        subtitle.setProperty("class", "subtitle")
        layout.addWidget(subtitle)
        
        layout.addStretch()
        self.setLayout(layout)
