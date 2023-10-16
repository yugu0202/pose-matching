import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2
import socket
import json
import mediapipe as mp
import numpy as np
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2

cwd = os.getcwd()
model_path = os.path.join(cwd, "./pose_landmarker_heavy.task")
cap = cv2.VideoCapture(3)

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

HOST = "127.0.0.1"
PORT = 53000

def draw_landmarks_on_image(rgb_image, detection_result):
  pose_landmarks_list = detection_result.pose_landmarks
  annotated_image = np.copy(rgb_image)

  # Loop through the detected poses to visualize.
  for idx in range(len(pose_landmarks_list)):
    pose_landmarks = pose_landmarks_list[idx]

    # Draw the pose landmarks.
    pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    pose_landmarks_proto.landmark.extend([
      landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
    ])
    solutions.drawing_utils.draw_landmarks(
      annotated_image,
      pose_landmarks_proto,
      solutions.pose.POSE_CONNECTIONS,
      solutions.drawing_styles.get_default_pose_landmarks_style())
  return annotated_image

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

options = PoseLandmarkerOptions(
        base_options = BaseOptions(model_asset_path = model_path),
        running_mode = VisionRunningMode.IMAGE,
)

with PoseLandmarker.create_from_options(options) as landmarker:
    while True:
        ret, frame = cap.read()
        if not ret:
           continue

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

        pose_landmarker_result = landmarker.detect(mp_image)

        annotated_image = draw_landmarks_on_image(mp_image.numpy_view(), pose_landmarker_result)
        cv2.imshow("mediapipe", cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))
        cv2.waitKey(5)

        send = {}

        if pose_landmarker_result.pose_world_landmarks:
            send["ok"] = True
            send["landmarks"] = [[l.x, l.y, l.z] for l in pose_landmarker_result.pose_world_landmarks[0]]
        else:
           send["ok"] = False
           send["landmarks"] = []

        print(send)
        client.sendto(json.dumps(send).encode("utf-8"), (HOST,PORT))

cap.release()
