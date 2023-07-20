import numpy as np
import mediapipe as mp
import time
import cv2

cap = cv2.VideoCapture(0)

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh()

# 1. 사람 얼굴을 찾았어.
# 2. 마스크로 쓸 이미지를 가져와야지.
# 3. 그 이미지를 씌울 위치를 찾아야겠지. 전체 얼굴에서 어느 위치에 (눈을 중심?, 코를 중심?)으로 할지 좌표값을 찾느다.
# 4. 그 다음 그 이미지를 마스크의 영역만큼을 픽셀값을 카피해서 덮어 씌워주면 된다.

faceimg = cv2.imread('face_mk.png', cv2.IMREAD_UNCHANGED)

# 찾은 얼굴에 가져올 이미지로 대체해주는 함수
# 주의 할점 : 이미지가 내가 찾은 좌표를 넘어가버리면 행렬 넘어가버리면 out of range같은 오류가 나온다.
def face_overlay(background_img, img_to_overlay, x, y, overlay_size=None):
    try:
        bg_img = background_img.copy()
        ov_img = img_to_overlay.copy()
        # backgorud img의 채널은 3채널(b,g,r) overlay의 이미지는 4채널이라 둘이 다르다.
        # backgorud img의 채널을 하나 늘려야한다.
        if bg_img.shape[2] == 3:
            bg_img = cv2.cvtColor(bg_img, cv2.COLOR_BGR2BGRA) # 알파 채널 추가해준다.

        # overlay_size는 가져올 이미지의 사이즈 조절
        if overlay_size is not None:
            img_to_overlay = cv2.resize(ov_img, overlay_size)

        # b,g,r,a 채널로 순서 분류
        b,g,r,a = cv2.split(img_to_overlay)

        # a체널 해당 부분에 블러 처리
        mask = cv2.medianBlur(a, 5)

        # 이미지 중심 좌표와 사람 얼굴 중심을 맞추기 위해 이미지 중심을 찾는다.
        h,w,_ = img_to_overlay.shape

        i_s = int(y - h / 2)
        i_e = int(y + h / 2)
        c_s = int(x - w / 2)
        c_e = int(x + w / 2)

        if i_s < 0:
            i_s = 0
        if i_e > bg_img.shape[0]:
            i_e = bg_img.shape[0]
        if c_s < 0:
            c_s = 0
        if c_e > bg_img.shape[1]:
            c_e = bg_img.shape[1]

        roi = bg_img[i_s:i_e,c_s :c_e]

        print(roi.shape, mask.shape)

        # 관심영역에서 마스크 되어있는 픽셀 들만 가져와서 붙이면 된다.
        # img1_bg 미키마우스가 아닌 곳의 관심영역에서 img1_bg를 해준 이유는 색깔이 바뀌기 때문이다.
        img1_bg = cv2.bitwise_and(roi.copy(),roi.copy(), mask = cv2.bitwise_not(mask))
        img2_fg = cv2.bitwise_and(img_to_overlay, img_to_overlay, mask=mask)

        # 캠이미지에 마스크영역과 마스크를 제외해서 더한 결과값을 갱신
        bg_img[i_s:i_e, c_s:c_e] = cv2.add(img1_bg, img2_fg)

        # a채널때문에 다시 바꿔줘
        bg_img = cv2.cvtColor(bg_img, cv2.COLOR_BGRA2RGB)

        return bg_img

    except:
        return background_img

while True:
    ret, img = cap.read()

    # 캡처된 이미지를 bgr로 되어있는 것을 rgb로 바꿔줘야 진행이 가능하다. 중요!!
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = faceMesh.process(imgRGB)
    ih, iw, ic = img.shape

    # 얼굴 landmark 찾기?
    if result.multi_face_landmarks:
        for faceLms in result.multi_face_landmarks:
            xy_point = []

            for c,lm in enumerate(faceLms.landmark):
                xy_point.append([lm.x, lm.y])

                # 찾은 이미지를 점으로 표시 눈으로 한번 보자
                # img = cv2.circle(img,(int(lm.x*iw), int(lm.y*ih)), 1, (255,0,0), 3)

            # 얼굴 맨위 왼쪽
            top_left = np.min(xy_point, axis=0)
            # 얼굴 아래 오른쪽
            bottom_right = np.max(xy_point, axis=0)
            # 얼굴 가운데
            mean_xy = np.mean(xy_point, axis=0)

            # 얼굴 가운데를 찾은곳을 빨간색으로 표시해보기
            # 얼굴 가운데를 찾은곳을 빨간색으로 표시해보기
            # img = cv2.circle(img, (int(mean_xy[0]*iw), int(mean_xy[1]*ih)),4,(0,0,255),3)

            face_width = int(bottom_right[0] * iw) - int(top_left[0] * iw)
            face_height = int(bottom_right[1] * ih) - int(top_left[1] * ih)

            if face_width > 0 and face_height > 0:

                result = face_overlay(img, faceimg,int(mean_xy[0]*iw),int(mean_xy[1]*ih),(face_width,face_height))

    try:
        cv2.imshow('face', result)
    except:
        cv2.imshow('face', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
