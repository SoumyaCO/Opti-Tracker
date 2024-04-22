import mediapipe as mp
import time  # for timestamps
import cv2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

MODEL_PATH = "../models/face_landmarker.task"

BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
FaceLandmarkerResult = mp.tasks.vision.FaceLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode


# Create a face landmarker instance with the live stream mode:
def print_result(
    result: FaceLandmarkerResult, output_image: mp.Image, timestamp_ms: int
):
    print("face landmarker result: {}".format(result))


options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result,
)

with FaceLandmarker.create_from_options(options) as landmarker:
    cap = cv2.VideoCapture(1)
    _, frame = cap.read()
    cv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # getting image from opencv and converting it to mp_image(mediapipe readable image)
    mp_image = mp.Image(image_format=mp.ImageFormat.GRAY8, data=cv_img)

    landmarker.detect(mp_image, time.time())
