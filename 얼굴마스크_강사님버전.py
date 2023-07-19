import cv2
import mediapipe as mp
import time
import numpy as np

cap = cv2.VideoCapture(0)
pTime = 0

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh()

faceimg = cv2.imread('face_mk.png',cv2.IMREAD_UNCHANGED)


def overlay_transparent(background_img, img_to_overlay_t, x, y, overlay_size=None):
    try :
        bg_img = background_img.copy()

        #bgr로 들어오는 이미지를 rgba로 수정
        if bg_img.shape[2] == 3:
            bg_img = cv2.cvtColor(bg_img, cv2.COLOR_BGR2BGRA)

        #face 이미지 사이즈가 재설정 되었으면 재설정된 이미지로 변경
        if overlay_size is not None:
            img_to_overlay_t = cv2.resize(img_to_overlay_t.copy(), overlay_size)

        #마스크 사용을 위해 채널 분리
        b, g, r, a = cv2.split(img_to_overlay_t)

        #마스크 블러처리
        mask = cv2.medianBlur(a, 5)

        #얼굴 영역 중심정 설정
        h, w, _ = img_to_overlay_t.shape
        roi = bg_img[int(y-h/2):int(y+h/2), int(x-w/2):int(x+w/2)]

        img1_bg = cv2.bitwise_and(roi.copy(), roi.copy(), mask=cv2.bitwise_not(mask))
        img2_fg = cv2.bitwise_and(img_to_overlay_t, img_to_overlay_t, mask=mask)

        #캠이미지에 마스크영역과 마스크를 제외해서 더한 결과값을 갱신
        bg_img[int(y-h/2):int(y+h/2), int(x-w/2):int(x+w/2)] = cv2.add(img1_bg, img2_fg)

        # convert 4 channels to 4 channels
        bg_img = cv2.cvtColor(bg_img, cv2.COLOR_BGRA2BGR)
        return bg_img
    except Exception :
        return background_img



face_sizes = []
while True:
    sucess, img = cap.read()

    img = cv2.resize(img, (int(img.shape[1]), int(img.shape[0])))

    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    result = faceMesh.process(imgRGB)
    if result.multi_face_landmarks:
        for faceLms in result.multi_face_landmarks:
        #    mpDraw.draw_landmarks(img, faceLms, mpFaceMesh.FACEMESH_CONTOURS)
            xy_point = []

            for c,lm in enumerate(faceLms.landmark):
                    ih,iw,ic = img.shape

                    img = cv2.circle(img,(int(lm.x * iw) , int(lm.y * ih) ),1,(255,0,0),3)
                    xy_point.append([lm.x,lm.y])

            top_left = np.min(xy_point,axis=0)
            bottom_right = np.max(xy_point, axis=0)
            mean_xy = np.mean(xy_point,axis=0)


            cv2.circle(img,center=(int(top_left[0] * iw) , int(top_left[1] * ih) ),radius=4, color=(0,0,255),thickness=2,lineType=cv2.LINE_AA)
            cv2.circle(img, center=(int(bottom_right[0] * iw), int(bottom_right[1] * ih)), radius=4, color=(0, 0, 255), thickness=2,lineType=cv2.LINE_AA)
            cv2.circle(img, center=(int(mean_xy[0] * iw), int(mean_xy[1] * ih)), radius=4, color=(0, 0, 255),thickness=2, lineType=cv2.LINE_AA)

            face_width = int(bottom_right[0] * iw) - int(top_left[0] * iw)
            face_height = int(bottom_right[1] * ih) - int(top_left[1] * ih)

            if face_width>0 and face_height>0:
                result = overlay_transparent(img, faceimg, int(mean_xy[0] * iw), int(mean_xy[1] * ih),overlay_size=(face_width+30, face_height+30))

                #result, color = cv2.pencilSketch(result, sigma_s=20, sigma_r=0.05, shade_factor=0.015)

    cv2.imshow('image', result)
    cTime = time.time()
    fps = 1 / (cTime - pTime)

    if cv2.waitKey(1) == ord('q'):
        break