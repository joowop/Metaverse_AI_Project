import cv2
import mediapipe as mp
import numpy as np
import math
import socket

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sendport = ('127.0.0.1', 5053)

cap = cv2.VideoCapture(0)

with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while True:
        ret, image = cap.read()

        image = cv2.flip(image, 1)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                p1 = hand_landmarks.landmark[4]
                p2 = hand_landmarks.landmark[8]

                a = p1.x - p2.x
                b = p1.y - p2.y
                c = math.sqrt((a * a) + (b * b))
                vol = int(c * 100)
                vol = np.abs(vol)

                senddata = str(vol)
                sock.sendto(str.encode(senddata), sendport)

                f1 = np.array([[p1.x, p1.y, p1.z]])
                f2 = np.array([[p2.x, p2.y, p2.z]])
                print(np.linalg.norm(f2 - f1))

                cv2.putText(image, text='Volum : %d' % vol,
                            org=(10, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=255, thickness=2)

                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow('hand', image)
        if cv2.waitKey(1) == ord('q'):
            break