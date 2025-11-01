import sys
import random
import vlc
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton
)
from PyQt5.QtGui import QPalette, QColor

# Huggingface transformer for emotion detection
from transformers import pipeline

# -------------------------
# Load Emotion Detection Model (Huggingface)
# -------------------------
print("Loading emotion model... (this may take 10-30s on first run)")
emotion_classifier = pipeline('text-classification', model='j-hartmann/emotion-english-distilroberta-base')

# Optional: Add or modify emotion mapping for music
emotion_to_tracks = {
    "joy": [
        "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
    ],
    "happiness": [
        "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
    ],
    "sadness": [
        "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3"
    ],
    "anger": [
        "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3"
    ],
    "fear": [
        "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3"
    ],
    "surprise": [
        "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
    ],
    "neutral": [
        "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3"
    ]
}

# Fallback for mapping model output to supported moods
def map_emotion(label):
    mapping = {
        "joy": "joy",
        "happiness": "joy",
        "sadness": "sadness",
        "anger": "anger",
        "fear": "fear",
        "surprise": "surprise",
        "neutral": "neutral"
    }
    return mapping.get(label.lower(), "neutral")

def detect_emotion(text):
    # If empty input, return neutral
    if not text.strip():
        return "neutral"
    # Use NLP model
    results = emotion_classifier(text)
    best = max(results, key=lambda x: x['score'])
    # print("DEBUG:", results)
    return map_emotion(best["label"])

def get_song_for_emotion(emotion):
    return random.choice(emotion_to_tracks.get(emotion, emotion_to_tracks["neutral"]))

# -------------------------
# GUI App
# -------------------------
class MoodifyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Moodify – Mood Music Player")
        self.setGeometry(100, 100, 400, 300)

        self.player = None

        self.layout = QVBoxLayout()

        self.label = QLabel("How are you feeling today?")
        self.layout.addWidget(self.label)

        self.mood_input = QLineEdit()
        self.layout.addWidget(self.mood_input)

        self.play_button = QPushButton("Play Mood Song")
        self.play_button.clicked.connect(self.play_song)
        self.layout.addWidget(self.play_button)

        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_song)
        self.layout.addWidget(self.pause_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_song)
        self.layout.addWidget(self.stop_button)

        self.setLayout(self.layout)

    # -------------------------
    # Play Song Based on Mood
    # -------------------------
    def play_song(self):
        mood_text = self.mood_input.text()
        if not mood_text.strip():
            self.label.setText("Please enter your mood!")
            return

        emotion = detect_emotion(mood_text)
        song_url = get_song_for_emotion(emotion)

        if self.player:
            self.player.stop()

        self.player = vlc.MediaPlayer(song_url)
        self.player.play()

        self.label.setText(f"Detected mood: {emotion.capitalize()}. Playing a matching song...")

        # Pastel background colors
        pastel_colors = {
            "joy": "#FFFACD",          # LemonChiffon
            "happiness": "#FFFACD",
            "sadness": "#ADD8E6",      # LightBlue
            "anger": "#FFB6C1",        # LightPink
            "fear": "#FFE4E1",         # MistyRose
            "surprise": "#FFDAB9",     # PeachPuff
            "neutral": "#E0E0E0"       # LightGray
        }
        self.change_background_color(pastel_colors.get(emotion, "#FFFFFF"))

    # -------------------------
    # Pause / Stop Controls
    # -------------------------
    def pause_song(self):
        if self.player:
            self.player.pause()

    def stop_song(self):
        if self.player:
            self.player.stop()

    def change_background_color(self, color_hex):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color_hex))
        self.setPalette(palette)

# -------------------------
# Run the App
# -------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MoodifyApp()
    window.show()
    sys.exit(app.exec())

