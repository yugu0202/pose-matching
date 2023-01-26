import cv2
import mediapipe as mp
import numpy as np
import time

def landmark2np(pose_landmarks):
    li = []
    for j in (pose_landmarks.landmark):
        li.append([j.x, j.y, j.z])

    return np.array(li) - li[0]


def manual_cos(A, B):
    dot = np.sum(A*B, axis=-1)
    A_norm = np.linalg.norm(A, axis=-1)
    B_norm = np.linalg.norm(B, axis=-1)
    cos = dot / (A_norm*B_norm+1e-7)
    print(cos[1:].mean())

    return cos[1:].mean()

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# For webcam input:
cap = cv2.VideoCapture(3)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)

saved_array = [None, None, None]
start = -100
score = [0, 0, 0]
saved_no = 0

with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = pose.process(image)

        # Draw the pose annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            for i, lm in enumerate(results.pose_landmarks.landmark):
                height, width, channel = image.shape
                cx, cy = int(lm.x * width), int(lm.y * height)
                cv2.putText(image, str(i+1), (cx+10, cy+10), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 5, cv2.LINE_AA)
                cv2.circle(image, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)


            if cv2.waitKey(1) & 0xFF == ord('s'):
                saved_array[0] = landmark2np(results.pose_landmarks)
                start = time.time()
                saved_no = 1
                print('no.1 saved')
            
            if cv2.waitKey(1) & 0xFF == ord('d'):
                saved_array[1] = landmark2np(results.pose_landmarks)
                start = time.time()
                saved_no = 2
                print('no.2 saved')
            
            if cv2.waitKey(1) & 0xFF == ord('f'):
                saved_array[2] = landmark2np(results.pose_landmarks)
                start = time.time()
                saved_no = 3
                print('no.3 saved')

            # cos類似度でチェック
            if saved_array[0] is not None:
                now_array = landmark2np(results.pose_landmarks)
                score[0] = manual_cos(saved_array[0], now_array)

            if saved_array[1] is not None:
                now_array = landmark2np(results.pose_landmarks)
                score[1] = manual_cos(saved_array[1], now_array)

            if saved_array[2] is not None:
                now_array = landmark2np(results.pose_landmarks)
                score[2] = manual_cos(saved_array[2], now_array)

        # 3s 表示
        if time.time() - start < 3:
            cv2.putText(image, f'No.{saved_no} saved', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3.0, (255, 255, 255), thickness=2)

        elif score[0] > 0.99:
            cv2.putText(image, 'no.1 pose', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3.0, (255, 0, 255), thickness=2)

        elif score[1] > 0.99:
            cv2.putText(image, 'no.2 pose', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3.0, (255, 0, 255), thickness=2)

        elif score[2] > 0.99:
            cv2.putText(image, 'no.3 pose', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3.0, (255, 0, 255), thickness=2)

        cv2.imshow('MediaPipe Pose', image)
        # ctrl and c to close a window
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
