# Importing libraries
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
from pydub import AudioSegment
from pydub.playback import play


# Sound files
audio_for_distracted = AudioSegment.from_ogg("./Audio/Distracted.ogg")
audio_for_sleepy = AudioSegment.from_ogg("./Audio/Sleepy.ogg")
audio_for_posture = AudioSegment.from_ogg("./Audio/Posture.ogg")

# GLOBAL FLAGS
EYE = "open"
HEAD = "front"


# Function to create the detection landmarks on the image .
def draw_landmarks_on_image(rgb_image, detection_result):
    face_landmarks_list = detection_result.face_landmarks
    annotated_image = np.copy(rgb_image)

    # Loop through the detected faces to visualize.
    for idx in range(len(face_landmarks_list)):
        face_landmarks = face_landmarks_list[idx]

        # Draw the face landmarks.
        face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        face_landmarks_proto.landmark.extend(
            [
                landmark_pb2.NormalizedLandmark(
                    x=landmark.x, y=landmark.y, z=landmark.z
                )
                for landmark in face_landmarks
            ]
        )

        solutions.drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks_proto,
            connections=mp.solutions.face_mesh.FACEMESH_IRISES,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_iris_connections_style(),
        )

    return annotated_image


def eye_lid_face_ratio(detection_results, frame_height, frame_width):
    face_top_x = detection_results.face_landmarks[0][10].x * frame_width
    face_top_y = detection_results.face_landmarks[0][10].y * frame_height

    face_bottom_x = detection_results.face_landmarks[0][152].x * frame_width
    face_bottom_y = detection_results.face_landmarks[0][152].y * frame_height

    face_distance = np.sqrt(
        (face_top_x - face_bottom_x) ** 2 + (face_top_y - face_bottom_y) ** 2
    )

    left_eye_up_y = detection_result.face_landmarks[0][386].y * frame_height
    left_eye_down_y = detection_result.face_landmarks[0][374].y * frame_height
    eye_distance = abs(left_eye_up_y - left_eye_down_y)

    ratio = eye_distance / face_distance
    print(
        f"---------------------------------------\n ---------RATIO: {ratio}-------- \n------------------------------"
    )


def left_eye_blink(detection_results, frame_height, frame_width):
    left_eye_up_y = detection_result.face_landmarks[0][386].y * frame_height
    left_eye_down_y = detection_result.face_landmarks[0][374].y * frame_height
    distance = abs(left_eye_up_y - left_eye_down_y)
    print(f"---------up-down-eye-distance ------{distance}--------------")

    if distance <= 10:
        EYE = "closed"
    else:
        EYE = "open"
    print(f"-------------{EYE}----------------")


def eye_distance(detection_result, frame_height, frame_width):
    left_eye_x = detection_result.face_landmarks[0][468].x * frame_width
    right_eye_x = detection_result.face_landmarks[0][473].x * frame_width

    left_eye_y = detection_result.face_landmarks[0][468].y * frame_height
    right_eye_y = detection_result.face_landmarks[0][473].y * frame_height

    distance = np.sqrt(
        (left_eye_x - right_eye_x) ** 2 + (right_eye_y - left_eye_y) ** 2
    )
    if distance <= 90:
        HEAD = "not-front"
    else:
        HEAD = "front"
    print(f"--------------{HEAD}---{distance}--------------")


BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
FaceLandmarkerResult = mp.tasks.vision.FaceLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

base_options = python.BaseOptions(model_asset_path="../models/face_landmarker.task")
options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    output_face_blendshapes=True,
    output_facial_transformation_matrixes=True,
    num_faces=1,
)
detector = vision.FaceLandmarker.create_from_options(options)

# Video capture via webcam (mine is 1, select according to your system , and camera)
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FPS, 1)
while cap.isOpened():
    ret, frame = cap.read()
    image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

    frame_height, frame_width, _ = frame.shape
    detection_result = detector.detect(image)
    try:
        left_eye_blink(detection_result, frame_height, frame_width)
        eye_distance(detection_result, frame_height, frame_width)

        # testing face top and bottom distance and eyea lid top and bottom ratio
        eye_lid_face_ratio(detection_result, frame_height, frame_width)
    except:
        print("CAN NOT FIND IT")

    # Annotate the image to show the tracking marks
    annotated_image = draw_landmarks_on_image(image.numpy_view(), detection_result)
    cv2.imshow("iris detection", cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
