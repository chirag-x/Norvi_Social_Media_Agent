from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QScrollArea, QFrame, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, QPropertyAnimation, QAbstractAnimation, QEasingCurve
from PySide6.QtGui import QIcon

class CollapsibleSection(QWidget):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        
        self.is_expanded = False
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header Button
        self.toggle_btn = QPushButton(title)
        self.toggle_btn.setProperty("class", "collapsible_btn")
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 15px;
                font-weight: bold;
                font-size: 15px;
                border-radius: 8px;
            }
        """)
        self.toggle_btn.clicked.connect(self.toggle)
        main_layout.addWidget(self.toggle_btn)
        
        # Content Area
        self.content_area = QFrame()
        self.content_area.setProperty("class", "collapsible_content")
        self.content_area.setStyleSheet("""
            QFrame {
                border-top: none;
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
            }
        """)
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        
        self.content_area.setVisible(False)
        main_layout.addWidget(self.content_area)
        
    def addWidget(self, widget: QWidget):
        self.content_layout.addWidget(widget)
        
    def addLayout(self, layout):
        self.content_layout.addLayout(layout)
        
    def toggle(self):
        self.is_expanded = not self.is_expanded
        
        if self.is_expanded:
            self.content_area.setVisible(True)
            self.toggle_btn.setStyleSheet("""
                QPushButton {
                    background-color: #1E293B;
                    color: white;
                    text-align: left;
                    padding: 15px;
                    font-weight: bold;
                    font-size: 15px;
                    border: 1px solid #374151;
                    border-bottom-left-radius: 0px;
                    border-bottom-right-radius: 0px;
                    border-top-left-radius: 8px;
                    border-top-right-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #293548;
                }
            """)
        else:
            self.content_area.setVisible(False)
            self.toggle_btn.setStyleSheet("""
                QPushButton {
                    background-color: #1E293B;
                    color: white;
                    text-align: left;
                    padding: 15px;
                    font-weight: bold;
                    font-size: 15px;
                    border: 1px solid #374151;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #293548;
                }
            """)
