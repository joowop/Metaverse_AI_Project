import cv2
import numpy as np

cap = cv2.VideoCapture(0)

back_frame = cv2.imread('image/starry_night.jpg')
back_frame = cv2.resize(back_frame, (int (cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                                     int (cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))) # 카메라와 크로마키의 크기를 맞춰주기 위해
# 합성 변수
do_composit = True

while True:
    ret, frame = cap.read()

    if not ret:
        break

    if do_composit:
        mask = cv2.inRange(frame,(0,100,0), (128,255,128))
        cv2.copyTo(back_frame, mask, frame)

    cv2.imshow('chroma', frame)

    if cv2.waitKey(1) == ord(' '):
        do_composit = not do_composit

    elif cv2.waitKey(1) == 27:
        break

cap.release()
