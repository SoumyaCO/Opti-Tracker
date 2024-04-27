# Importing libraries
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2


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


def left_eye_blink(detection_results):
    print(type(detection_result))
    id1 = detection_result.face_landmarks[0][386].y
    id2 = detection_result.face_landmarks[0][374].y
    print(id1, id2)
    print(f"DISTANCE==========================\n{abs(id1 - id2)}")


def eye_distance(detection_result):
    left_eye_x = detection_result.face_landmarks[0][468].x
    right_eye_x = detection_result.face_landmarks[0][473].x

    left_eye_y = detection_result.face_landmarks[0][468].y
    right_eye_y = detection_result.face_landmarks[0][473].y

    distance = np.sqrt(
        (left_eye_x - right_eye_x) ** 2 + (right_eye_y - left_eye_y) ** 2
    )
    print(f"EYE DISTANCE===========\n{distance}")


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

while cap.isOpened():
    ret, frame = cap.read()
    image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

    detection_result = detector.detect(image)
    try:
        eye_distance(detection_result)
    except:
        print("NOT STARTED")

    # Annotate the image to show the tracking marks
    annotated_image = draw_landmarks_on_image(image.numpy_view(), detection_result)
    cv2.imshow("iris detection", cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
