import cv2
import numpy as np
import mediapipe as mp
import math

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

def three_angle(a,b,c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1] , c[0] - b[0]) - np.arctan2(a[1] - b[1] , a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

with mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as pose:
    while True:
        ret,frame = cap.read()

        image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        result = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        mp_drawing.draw_landmarks(image,result.pose_landmarks,mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(255,0,0),thickness=2,circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                                  )

        try:
            landmarks = result.pose_landmarks.landmark

            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x , landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y ]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x , landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y ]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            va = np.array(elbow) - np.array(shoulder)
            vb = np.array(elbow) - np.array(wrist)

            norm_a = np.linalg.norm(va)
            norm_b = np.linalg.norm(vb)

            dot_ab = np.dot(va,vb)
            temp = dot_ab/(norm_a * norm_b)
            rad = math.acos(temp)
            deg = math.degrees(rad)

            print (three_angle(shoulder , elbow , wrist))

        except:
            pass

        cv2.imshow('pose',image)

        if cv2.waitKey(10) & 0XFF == ord('q'):
            break




