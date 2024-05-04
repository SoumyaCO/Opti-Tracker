# Importing libraries
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from pydub import AudioSegment
from pydub.playback import play

# Sound files
audio_for_distracted = AudioSegment.from_ogg("./Audio/Distracted.ogg")
audio_for_sleepy = AudioSegment.from_ogg("./Audio/Sleepy.ogg")
audio_for_posture = AudioSegment.from_ogg("./Audio/Posture.ogg")

# GLOBAL FLAGS
EYE = "open"
HEAD = "front"
TIME_COUNTER = 0  # time in seconds

# Testing for the local variable condition  ---------------------------------
print(f"Time counter from 'face_landmarks.py' file: {TIME_COUNTER}")
# ---------------------------------------------------------


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


def play_audio(name):
    """
    plays the audio (preprocessed by pydub)
    later: have to make it async.(or threading)
    """
    play(name)


def calculate_ratio(detection_results, frame_height, frame_width, distance):
    """
    Calulates the ratio of a facial distance
    with respect to the distance between forehead and chin.
    """
    face_top_x = detection_results.face_landmarks[0][10].x * frame_width
    face_top_y = detection_results.face_landmarks[0][10].y * frame_height

    face_bottom_x = detection_results.face_landmarks[0][152].x * frame_width
    face_bottom_y = detection_results.face_landmarks[0][152].y * frame_height

    face_distance = np.sqrt(
        (face_top_x - face_bottom_x) ** 2 + (face_top_y - face_bottom_y) ** 2
    )
    return round(distance / face_distance * 100, 2)


def left_eye_blink(detection_result, frame_height, frame_width):
    """
    Calculate distance between the left eye upper eye-lid and lower eye-lid.
    """
    left_eye_up_y = detection_result.face_landmarks[0][386].y * frame_height
    left_eye_down_y = detection_result.face_landmarks[0][374].y * frame_height
    distance = abs(left_eye_up_y - left_eye_down_y)
    return distance


def eye_distance(detection_result, frame_height, frame_width):
    """
    Calculates the distance between two iris
    -> (helps to indirtectly determine the head position of a person)
    """
    left_eye_x = detection_result.face_landmarks[0][468].x * frame_width
    right_eye_x = detection_result.face_landmarks[0][473].x * frame_width

    left_eye_y = detection_result.face_landmarks[0][468].y * frame_height
    right_eye_y = detection_result.face_landmarks[0][473].y * frame_height

    distance = np.sqrt(
        (left_eye_x - right_eye_x) ** 2 + (right_eye_y - left_eye_y) ** 2
    )
    return distance

BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
FaceLandmarkerResult = mp.tasks.vision.FaceLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

base_options = python.BaseOptions(
    model_asset_path="models/face_landmarker.task")
options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    output_face_blendshapes=True,
    output_facial_transformation_matrixes=True,
    num_faces=1,
)
detector = vision.FaceLandmarker.create_from_options(options)

# function for capturing camera 
def camera_function(frame):
    image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
    frame_height, frame_width, _ = frame.shape
    detection_result = detector.detect(image)
    ratio_eye_lid_distance = 100
    ratio_bw_eyes = 100
    try:
        left_eye_lid_distance = left_eye_blink(
            detection_result, frame_height, frame_width
        )
        distance_bw_eyes = eye_distance(
            detection_result, frame_height, frame_width)

        # Calculate the ratio and print it .
        ratio_eye_lid_distance = calculate_ratio(
            detection_result, frame_height, frame_width, left_eye_lid_distance
        )
        ratio_bw_eyes = calculate_ratio(
            detection_result, frame_height, frame_width, distance_bw_eyes
        )

        # bareaking the scope of these ywo variables 
        ratio_bw_eyes = ratio_bw_eyes
        ratio_eye_lid_distance = ratio_eye_lid_distance

       # if ratio_bw_eyes < 35:
       #     TIME_COUNTER += 1 / 15
       # else:
       #     TIME_COUNTER = 0

       # if TIME_COUNTER >= 10:
       #     play(audio_for_distracted)
       #     TIME_COUNTER = 0

        #print("=== EYE_LID_DISTANCE: {}".format(ratio_eye_lid_distance))
        #print("====DISTANCE_BW_EYES: {}".format(ratio_bw_eyes))

    except Exception as e:
        print("exception occured")
        print(e)
        # Annotate the image to show the tracking marks
    annotated_image = draw_landmarks_on_image(image.numpy_view(), detection_result)
    return ratio_bw_eyes, ratio_eye_lid_distance, annotated_image

