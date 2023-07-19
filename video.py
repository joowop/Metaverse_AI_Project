import cv2

vcap = cv2.VideoCapture(0) # 기본 카메라 열기

w = round(vcap.get(cv2.CAP_PROP_FRAME_WIDTH)) # cam width
h = round(vcap.get(cv2.CAP_PROP_FRAME_HEIGHT)) # cam height

# 코덱을 맞춰줘야 한다.
codec = cv2.VideoWriter_fourcc(*'DIVX') # avi 저장
# codec = cv2.VideoWriter_fourcc(*'FMP4') # mp4로 저장

fps = round(vcap.get(cv2.CAP_PROP_FPS))
delay = round(1000/fps)

# 저장
out = cv2.VideoWriter('out.avi', codec, fps, (w,h))


while True :
    ret, frame = vcap.read()

    if not ret :
        break

    # 화면 좌우반전 시키기
    frame = cv2.flip(frame, 1) # 1이 좌우반전, 0이 상하반전
    # inference 작업
    out.write(frame)
    cv2.imshow('cam', frame)


    if cv2.waitKey(1) == 27:
        break

out.release()
vcap.release()