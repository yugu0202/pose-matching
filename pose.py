import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2
import socket
import json
import mediapipe as mp
import numpy as np
import time

cwd = os.getcwd()
model_path = os.path.join(cwd, "./pose_landmarker_heavy.task")
cap = cv2.VideoCapture(3)

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
PoseLandmarkerResult = mp.tasks.vision.PoseLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

HOST = "127.0.0.1"
PORT = 53000

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def print_result(result: PoseLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    print("callback")
    send = {}
    send["landmarks"] = [[l.x, l.y, l.z] for l in result.pose_world_landmarks[0]]
    print(send)
    client.sendto(json.dumps(send).encode("utf-8"), (HOST,PORT))


options = PoseLandmarkerOptions(
        base_options = BaseOptions(model_asset_path = model_path),
        running_mode = VisionRunningMode.LIVE_STREAM,
        result_callback = print_result
)

with PoseLandmarker.create_from_options(options) as landmarker:
    while True:
        ret, frame = cap.read()
        frame_timestamp_ms = int(cap.get(cv2.CAP_PROP_POS_MSEC))

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)


        landmarker.detect_async(mp_image, frame_timestamp_ms)


cap.release()
