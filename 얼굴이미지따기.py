import cv2
import mediapipe as mp

import time
import numpy as np

vcap = cv2.VideoCapture(0)

mpDraw = mp.solutions.drawing_utils
mpFaceMash = mp.solutions.face_mesh
faceMash = mpFaceMash.FaceMesh()

while True:
    sucess, img = vcap.read()

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = faceMash.process(imgRGB)

    if result.multi_face_landmarks:
        for faceLms in result.multi_face_landmarks:
            xy_point = []
            for c, lm in enumerate(faceLms.landmark):
                xy_point.append([lm.x, lm.y])
                print(c,lm.x, lm.y)
        top_left = np.min(xy_point, axis=0)
        bottom_right = np.max(xy_point, axis = 0)
        mean_xy = np.mean(xy_point, axis=0)

    ih, iw, ic = img.shape

    face_width = int(bottom_right[0] * iw) - int(top_left[0]*iw)
    face_height = int(bottom_right[1] * ih) - int(top_left[1] * ih)

    sx = int(top_left[0] * iw)
    sy = int(top_left[1] * ih)

    roi = img[ sy : sy+face_height , sx : sx+face_width]

    roi = cv2.resize(roi, (int (face_width/14), int(face_height/10)))
    roi = cv2.resize(roi, (face_width,face_height), interpolation=cv2.INTER_AREA)



    try:
        img[ sy : sy+face_height , sx : sx+face_width] = roi
    except:
        pass

    cv2.imshow('face', img)

    if cv2.waitKey(1) == ord('q'):
        break

vcap.release()
cv2.destroyAllWindows()