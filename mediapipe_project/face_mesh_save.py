import mediapipe as mp
import cv2
import numpy as np
from os import path
import csv

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

cap = cv2.VideoCapture(0)

# face mesh 정확도 예측
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while True:
        ret,frame = cap.read()

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        result = holistic.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        mp_drawing.draw_landmarks(image, result.face_landmarks, mp_holistic.FACEMESH_CONTOURS,
                                  mp_drawing.DrawingSpec(color=(255,0,0), thickness=1, circle_radius=1),
                                  mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=1, circle_radius=1))

        try:
            face = result.face_landmarks.landmark
            face_list = []
            for temp in face:
                face_list.append([temp.x, temp.y, temp.z])

            face_row = list(np.array(face_list).flatten())

            # csv 파일 만들기
            if path.isfile('facedata.csv') == False:
                landmarks = ['class']
                for val in range(1, len(face) + 1):
                    landmarks += ['x{}'.format(val), 'y{}'.format(val), 'z{}'.format(val)]

                with open('facedata.csv', mode='w', newline='') as f:
                    csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    csv_writer.writerow(landmarks)
                f.close()
            else:
                if cv2.waitKey(1) & 0xFF == ord('1'):
                    print('save1')
                    face_row.insert(0, 'happy')
                    with open('facedata.csv', mode='a', newline='') as f:
                        csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        csv_writer.writerow(face_row)
                    f.close()
                elif cv2.waitKey(1) & 0xFF == ord('2'):
                    print('save2')
                    face_row.insert(0, 'sad')
                    with open('facedata.csv', mode='a', newline='') as f:
                        csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        csv_writer.writerow(face_row)
                    f.close()

        except:
            pass

        cv2.imshow('face', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break