import sys
import cv2
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, 
    QComboBox, QSizePolicy, QHBoxLayout, QLineEdit, QFormLayout, QFileDialog
)
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtCore import QPropertyAnimation, QRect
from PyQt5.QtGui import QColor
from face_landmarks import *  # Assuming you have the face_landmarks.py

class SplashScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Opti-Tracker")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: #2E3B4E;")  # Background color

        # Static splash screen label
        self.splash_label = QLabel(self)
        self.splash_label.setText("Welcome to Opti-Tracker")
        self.splash_label.setFont(QFont("Arial", 30, QFont.Bold))
        self.splash_label.setAlignment(Qt.AlignCenter)
        self.splash_label.setStyleSheet("color: white;")
        self.splash_label.setGeometry(0, 200, 1000, 100)  # Center text horizontally and vertically

        # Animation for other elements (if needed)
        self.animation_label = QLabel(self)
        self.animation_label.setText("Loading...")
        self.animation_label.setFont(QFont("Arial", 20))
        self.animation_label.setAlignment(Qt.AlignCenter)
        self.animation_label.setStyleSheet("color: lightgray;")
        self.animation_label.setGeometry(0, 300, 1000, 50)

        # Animation for animation_label
        self.animation = QPropertyAnimation(self.animation_label, b"geometry")
        self.animation.setDuration(2000)
        self.animation.setStartValue(QRect(0, 300, 1000, 50))
        self.animation.setEndValue(QRect(0, 500, 1000, 50))
        self.animation.finished.connect(self.hide_splash_screen)

        self.animation.start()

    def hide_splash_screen(self):
        self.animation_label.setVisible(False)
        self.show_main_window()

    def show_main_window(self):
        # Replace CameraWindow with your main application window
        self.main_window = CameraWindow()
        self.main_window.show()


class CameraWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Opti-Tracker")
        self.setMinimumWidth(1000)  # Increased width to accommodate the profile section
        self.setMinimumHeight(600)

        self.capture = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.TIME_COUNTER_SLEEP = 0
        self.TIME_COUNTER_DIST = 0

        self.profile_data = {"name": "", "age": "", "picture": None}
        self.init_ui()

    def init_ui(self):
        # Central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QHBoxLayout()

        # Profile Section
        profile_layout = QVBoxLayout()
        profile_layout.setAlignment(Qt.AlignTop)

        profile_title = QLabel("User Profile", self)
        profile_title.setFont(QFont("Arial", 16, QFont.Bold))
        profile_layout.addWidget(profile_title)

        self.profile_picture_label = QLabel(self)
        self.profile_picture_label.setAlignment(Qt.AlignCenter)
        self.profile_picture_label.setFixedSize(150, 150)
        self.profile_picture_label.setStyleSheet("border: 1px solid gray;")
        profile_layout.addWidget(self.profile_picture_label)

        select_picture_button = QPushButton("Select Picture", self)
        select_picture_button.clicked.connect(self.select_picture)
        profile_layout.addWidget(select_picture_button)

        form_layout = QFormLayout()
        self.name_input = QLineEdit(self)
        self.age_input = QLineEdit(self)
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Age:", self.age_input)
        profile_layout.addLayout(form_layout)

        save_profile_button = QPushButton("Save Profile", self)
        save_profile_button.clicked.connect(self.save_profile)
        profile_layout.addWidget(save_profile_button)

        self.profile_display = QLabel(self)
        self.profile_display.setAlignment(Qt.AlignTop)
        self.profile_display.setStyleSheet("border: 1px solid gray; padding: 10px;")
        profile_layout.addWidget(self.profile_display)

        main_layout.addLayout(profile_layout)

        # Camera Section
        camera_layout = QVBoxLayout()

        # Camera selection dropdown
        self.camera_dropdown = QComboBox(self)
        self.camera_dropdown.addItem("Select Camera")
        self.camera_dropdown.addItem("0")
        self.camera_dropdown.addItem("1")
        self.camera_dropdown.currentIndexChanged.connect(self.change_camera)
        camera_layout.addWidget(self.camera_dropdown)

        # Button layout to center the buttons
        button_layout = QHBoxLayout()

        # Start button
        self.start_button = QPushButton("Start Camera", self)   
        self.start_button.setFixedSize(150, 40)
        self.start_button.clicked.connect(self.start_camera)
        button_layout.addWidget(self.start_button)

        # Stop button
        self.stop_button = QPushButton("Stop Camera", self)
        self.stop_button.setFixedSize(150, 40)
        self.stop_button.clicked.connect(self.stop_camera)
        button_layout.addWidget(self.stop_button)

        # Center the buttons within the layout
        button_layout.setAlignment(Qt.AlignCenter)
        camera_layout.addLayout(button_layout)

        # Image display label
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        camera_layout.addWidget(self.image_label)

        main_layout.addLayout(camera_layout)

        central_widget.setLayout(main_layout)

    def select_picture(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Profile Picture", "", "Images (*.png *.jpg *.jpeg)")
        if file_name:
            pixmap = QPixmap(file_name)
            self.profile_picture_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.profile_data["picture"] = file_name

    def save_profile(self):
        name = self.name_input.text()
        age = self.age_input.text()
        if not name or not age:
            self.profile_display.setText("Please enter both name and age.")
        else:
            self.profile_data["name"] = name
            self.profile_data["age"] = age
            self.display_profile()

    def display_profile(self):
        profile_text = f"Name: {self.profile_data['name']}\nAge: {self.profile_data['age']}"
        self.profile_display.setText(profile_text)

    def start_camera(self):
        selected_camera = int(self.camera_dropdown.currentText()) if self.camera_dropdown.currentText() != "Select Camera" else 0
        self.capture = cv2.VideoCapture(selected_camera)
        if self.capture.isOpened():
            self.timer.start(33)

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
                self.TIME_COUNTER_DIST += 1 / 15.0
            elif distance_bw_lids < 4:
                self.TIME_COUNTER_SLEEP += 1 / 15.0
            else:
                self.TIME_COUNTER_DIST = 0
                self.TIME_COUNTER_SLEEP = 0

            if self.TIME_COUNTER_DIST >= 8:
                play_audio(audio_for_distracted)
                self.TIME_COUNTER_DIST = 0
            elif self.TIME_COUNTER_SLEEP >= 8:
                play_audio(audio_for_sleepy)
                self.TIME_COUNTER_SLEEP = 0
            cv2.putText(frame, f"Sleepiness Duration: {round(self.TIME_COUNTER_SLEEP, 1)}", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, f"Non-attentive Duration: {round(self.TIME_COUNTER_DIST, 1)}", (100, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

            # Convert frame to QImage
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap(q_img)
            self.image_label.setPixmap(pixmap)

    def change_camera(self):
        if self.capture:
            self.capture.release()
        self.start_camera()


from PyQt5.QtWidgets import QStackedWidget  # Add this import

# Final code to run the splash screen and main window together
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Create the main window and the splash screen
    splash = SplashScreen()
    main_window = CameraWindow()

    # Set up the stacked widget to switch between splash and main window
    stacked_widget = QStackedWidget()
    stacked_widget.addWidget(splash)
    stacked_widget.addWidget(main_window)

    # Show the stacked widget with splash screen initially
    stacked_widget.setCurrentWidget(splash)
    stacked_widget.resize(1000, 600)

    # Timer to switch from splash screen to main window after a delay
    QTimer.singleShot(3000, lambda: stacked_widget.setCurrentWidget(main_window))  # Switch after 3 seconds

    # Show the stacked widget
    stacked_widget.show()

    sys.exit(app.exec_())


