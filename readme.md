## Computer Vision based focus assistant

---
### Video Demo
[![Watch](https://github.com/SoumyaCO/mediapipe_project/assets/101652501/3913351b-3114-45c9-9a7d-cddb55435f4d)](https://youtu.be/WhsXiTHbgkQ?si=WR3RrG2dCLAvyq6b)



# Opti Tracker

**Opti Tracker** is an AI-powered application designed to **monitor and analyze** user activity in real-time using **facial landmark detection** and **tracking mechanisms**. It provides **feedback alerts** based on user posture, attention level, and fatigue, ensuring better focus and ergonomic posture.

## 🚀 Features
- 🎭 **Real-time Facial Landmark Tracking**: Uses **MediaPipe** to detect and analyze face movement.
- 🔊 **Audio Feedback Alerts**: Notifies users if they are **distracted, sleepy, or have poor posture**.
- 🖥️ **PyQt-based UI**: Provides an interactive interface for tracking and feedback visualization.
- 📂 **Modular Architecture**: Components are structured separately for better code organization.

---

## 📁 Project Directory Structure

```plaintext
opti-tracker/
├── README.md                   # Project documentation
├── face_landmarks.py            # Facial landmark detection script
├── icons.py                     # Handles icon resources
├── main.py                      # Main entry point for the application
├── requirements.txt              # List of dependencies
│
├── Audio/                        # Audio feedback alerts
│   ├── Distracted.ogg            # Alert for distraction
│   ├── Posture.ogg               # Alert for poor posture
│   └── Sleepy.ogg                # Alert for drowsiness
│
├── media/                        # Folder for media resources
├── mediapipe_experiments/        # Mediapipe experiment scripts
│   ├── face_landmarks.py         # Face landmark detection experiments
│   └── face_lm_rec.py            # Face recognition test script
│
└── models/                       # Pre-trained AI models
    └── face_landmarker.task      # Model for face landmark detection


```

# Installation

### 1. Clone the Repository

``` 
git clone https://github.com/yourusername/opti-tracker.git
cd opti-tracker 
```
### 2. Create a Virtual Environment

```
python3 -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate     # For Windows

```
### 3. Install Dependencies
```
pip install -r requirements.txt

```
# Dependencies

The project relies on the following key libraries:

* **PyQt5** – For GUI development.
* **OpenCV** - For Video Capture and processing.
* **MediaPipe** – For real-time facial landmark detection.
* **PyDub** – For playing audio feedback.
* **Additional** dependencies listed in `requirements.txt`.

# 🚀 Usage

To run the Opti Tracker, execute:

```
python main.py

```
This will launch the application and start tracking the user's face, detecting distractions, posture issues, or fatigue, and providing real-time feedback.

# 🛠️ How It Works

Uses MediaPipe to analyze 68 facial landmarks in real time.
Continuously monitors head position, eye movement, and posture.
Triggers audio alerts from the Audio/ folder when:

* User looks away (distracted)
* Slouches (poor posture)
* Shows signs of drowsiness (sleepy)

# 🤝 Contributing

We welcome contributions! Follow these steps:

### 1. Fork the repository.

```
https://github.com/SoumyaCO/Opti-Tracker.git

```

### 2. Create a new branch:

```
git checkout -b feature-name
```
### 3. Make your changes and commit:

```
git commit -m "Added new feature"
```
### 4. Push to the branch:

```
git push origin feature-name
```

### 5. Submit a Pull Request.
