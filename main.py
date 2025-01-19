import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QComboBox, QSizePolicy, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
from face_landmarks import *  # Assuming you have the face_landmarks.py

class CameraWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Opti-Tracker")
        self.setMinimumWidth(800)  # Set a minimum width
        self.setMinimumHeight(600)  # Set a minimum height

        self.capture = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.TIME_COUNTER_SLEEP = 0
        self.TIME_COUNTER_DIST = 0
        
        self.init_ui()

    def init_ui(self):
        # Central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # Camera selection dropdown
        self.camera_dropdown = QComboBox(self)
        self.camera_dropdown.addItem("Select Camera")
        self.camera_dropdown.addItem("0")
        self.camera_dropdown.addItem("1")
        self.camera_dropdown.currentIndexChanged.connect(self.change_camera)
        layout.addWidget(self.camera_dropdown)

        # Button layout to center the buttons
        button_layout = QHBoxLayout()
        
        # Start button
        self.start_button = QPushButton("Start Camera", self)
        self.start_button.setFixedSize(150, 40)  # Set fixed size for the button
        self.start_button.clicked.connect(self.start_camera)
        button_layout.addWidget(self.start_button)

        # Stop button
        self.stop_button = QPushButton("Stop Camera", self)
        self.stop_button.setFixedSize(150, 40)  # Set fixed size for the button
        self.stop_button.clicked.connect(self.stop_camera)
        button_layout.addWidget(self.stop_button)

        # Center the buttons within the layout
        button_layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(button_layout)

        # Image display label
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)  # Make sure the image is centered
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Make it resizable
        layout.addWidget(self.image_label)

        central_widget.setLayout(layout)

    def start_camera(self):
        selected_camera = int(self.camera_dropdown.currentText()) if self.camera_dropdown.currentText() != "Select Camera" else 0
        self.capture = cv2.VideoCapture(selected_camera)
        if self.capture.isOpened():
            self.timer.start(33)  # Update every 33ms (30fps)

    def stop_camera(self):
        if self.capture:
            self.capture.release()
        self.timer.stop()

    def update_frame(self):
        ret, frame = self.capture.read()
        if ret:
            # Process frame
            distance_bw_eyes, distance_bw_lids, frame = camera_function(frame)

            if distance_bw_eyes <= 38:
                self.TIME_COUNTER_DIST += 1/15.0
            elif distance_bw_lids < 4:
                self.TIME_COUNTER_SLEEP += 1/15.0
            else:
                self.TIME_COUNTER_DIST = 0
                self.TIME_COUNTER_SLEEP = 0

            if self.TIME_COUNTER_DIST>= 8:
                play_audio(audio_for_distracted)
                self.TIME_COUNTER_DIST = 0
            elif self.TIME_COUNTER_SLEEP >= 8:
                play_audio(audio_for_sleepy)
                self.TIME_COUNTER_SLEEP = 0
            cv2.putText(frame, f"Sleepyness Duration: {round(self.TIME_COUNTER_SLEEP, 1)}", (100, 100),cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, f"Non-attentive Duration: {round(self.TIME_COUNTER_DIST, 1)}", (100, 150),cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            
            # Resize the frame to fit the window
            window_width = self.width()
            window_height = self.height()

            aspect_ratio = frame.shape[1] / frame.shape[0]

            # Resize the frame to fit within the window
            new_width = window_width
            new_height = int(new_width / aspect_ratio)

            if new_height > window_height:
                new_height = window_height
                new_width = int(new_height * aspect_ratio)

            resized_frame = cv2.resize(frame, (new_width, new_height))

            # Convert frame to QImage format
            resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            height, width, channel = resized_frame.shape
            bytes_per_line = 3 * width
            q_img = QImage(resized_frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap(q_img)
            self.image_label.setPixmap(pixmap)

    def change_camera(self):
        if self.capture:
            self.capture.release()
        self.start_camera()

# Run the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CameraWindow()
    window.show()
    sys.exit(app.exec_())
