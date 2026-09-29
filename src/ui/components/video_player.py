from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QSlider
from PySide6.QtCore import Qt, QUrl, QTimer
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget

class PreviewDialog(QDialog):
    def __init__(self, video_path: str, start_time: float, end_time: float, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Clip Preview")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("background-color: #0B0F19; color: white;")
        
        self.video_path = video_path
        self.start_time = float(start_time)
        self.end_time = float(end_time)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Video Widget
        self.video_widget = QVideoWidget()
        layout.addWidget(self.video_widget, stretch=1)
        
        # Audio Output
        self.audio_output = QAudioOutput()
        
        # Media Player
        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.video_widget)
        self.player.setAudioOutput(self.audio_output)
        
        # Controls Layout
        controls = QHBoxLayout()
        
        self.play_btn = QPushButton("Play")
        self.play_btn.setFixedWidth(80)
        self.play_btn.setStyleSheet("background-color: #3B82F6; color: white; border-radius: 4px; padding: 5px;")
        self.play_btn.clicked.connect(self.toggle_play)
        controls.addWidget(self.play_btn)
        
        self.time_label = QLabel("00:00 / 00:00")
        controls.addWidget(self.time_label)
        
        # Slider
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.sliderMoved.connect(self.set_position)
        controls.addWidget(self.slider)
        
        layout.addLayout(controls)
        
        # Set up player
        self.player.setSource(QUrl.fromLocalFile(video_path))
        
        # Position tracking
        self.player.positionChanged.connect(self.position_changed)
        
        # Check end time constraint
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_end_time)
        self.timer.start(100)
        
        # We must wait for media to load before seeking
        self.player.mediaStatusChanged.connect(self._on_media_status_changed)
        
    def _on_media_status_changed(self, status):
        if status in (QMediaPlayer.MediaStatus.LoadedMedia, QMediaPlayer.MediaStatus.BufferedMedia):
            # Only seek once when it first loads
            if not hasattr(self, '_has_seeked'):
                self.player.setPosition(int(self.start_time * 1000))
                self._has_seeked = True
        
    def showEvent(self, event):
        super().showEvent(event)
        self.player.play()
        self.play_btn.setText("Pause")
        
    def closeEvent(self, event):
        self.player.stop()
        super().closeEvent(event)
        
    def toggle_play(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
            self.play_btn.setText("Play")
        else:
            self.player.play()
            self.play_btn.setText("Pause")
            
    def position_changed(self, position):
        duration = (self.end_time - self.start_time) * 1000
        current = position - (self.start_time * 1000)
        if duration > 0:
            percentage = max(0, min(100, int((current / duration) * 100)))
            self.slider.setValue(percentage)
            
            # Update label
            curr_s = max(0, current / 1000.0)
            dur_s = duration / 1000.0
            self.time_label.setText(f"{curr_s:.1f}s / {dur_s:.1f}s")
            
    def set_position(self, percentage):
        duration = (self.end_time - self.start_time) * 1000
        target = (self.start_time * 1000) + (duration * percentage / 100)
        self.player.setPosition(int(target))
        
    def check_end_time(self):
        if self.player.position() >= (self.end_time * 1000):
            self.player.pause()
            self.player.setPosition(int(self.start_time * 1000))
            self.play_btn.setText("Play")
