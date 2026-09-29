from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, QPoint, QRect
from PySide6.QtGui import QFont, QCursor


RESIZE_MARGIN = 6  # px from edge that triggers resize cursor


class CustomTitleBar(QWidget):
    """
    A sleek, frameless custom title bar with dragging support,
    branded logo/name, and styled min/max/close buttons.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._drag_pos = None
        self.setFixedHeight(44)
        self.setObjectName("title_bar")
        # Always dark regardless of light/dark theme — it's an OS-chrome element.
        # Setting directly on the widget overrides the global app stylesheet.
        self.setStyleSheet("""
            QWidget#title_bar {
                background-color: #0D1117;
                border-bottom: 1px solid #1F2937;
            }
            QWidget#title_bar QLabel {
                color: #F1F5F9;
                background-color: transparent;
            }
            QWidget#title_bar QPushButton {
                background-color: transparent;
                color: #9CA3AF;
                border: none;
                border-radius: 6px;
                font-size: 14px;
            }
        """)
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 0, 8, 0)
        layout.setSpacing(0)

        # Brand logo dot + name
        dot = QLabel("●")
        dot.setStyleSheet("color: #3B82F6; font-size: 14px; margin-right: 6px; border: none;")
        layout.addWidget(dot)

        brand = QLabel("Nexus")
        brand.setStyleSheet(
            "color: #F9FAFB; font-size: 14px; font-weight: 700; letter-spacing: 0.5px; border: none;"
        )
        layout.addWidget(brand)

        layout.addStretch()

        # Window controls
        for symbol, tooltip, slot, hover_color in [
            ("─", "Minimize", self._minimize, "#374151"),
            ("⬜", "Maximize / Restore", self._toggle_maximize, "#374151"),
            ("✕", "Close", self._close, "#DC2626"),
        ]:
            btn = QPushButton(symbol)
            btn.setToolTip(tooltip)
            btn.setFixedSize(40, 32)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: #9CA3AF;
                    border: none;
                    border-radius: 6px;
                    font-size: 14px;
                }}
                QPushButton:hover {{
                    background-color: {hover_color};
                    color: white;
                }}
            """)
            btn.clicked.connect(slot)
            layout.addWidget(btn)

    # ── drag-to-move ──────────────────────────────────────────────────────────
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.window().frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self._drag_pos and event.buttons() == Qt.MouseButton.LeftButton:
            win = self.window()
            if win.isMaximized():
                win.showNormal()
            win.move(event.globalPosition().toPoint() - self._drag_pos)

    def mouseReleaseEvent(self, event):
        self._drag_pos = None

    def mouseDoubleClickEvent(self, event):
        self._toggle_maximize()

    # ── window actions ────────────────────────────────────────────────────────
    def _minimize(self):
        self.window().showMinimized()

    def _toggle_maximize(self):
        win = self.window()
        if win.isMaximized():
            win.showNormal()
        else:
            win.showMaximized()

    def _close(self):
        self.window().close()
