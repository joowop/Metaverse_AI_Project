import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
'''
각도의 의미 학습을 시켜서 활용 가능하다.

손가락 제스쳐를 활용한 컨트롤러 등

주먹 stop

보자기 fire
'''
max_num_hands = 1
gesture = { 0:'stop' , 1:'fire' }

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

total_result = []
def click(event,x,y,flags,params):
    global data
    if event == cv2.EVENT_LBUTTONDOWN:
        print('mouse click')
        total_result.append(data)
        print(data)

cv2.namedWindow('Dataset')
cv2.setMouseCallback('Dataset',click)

with mp_hands.Hands(max_num_hands=max_num_hands, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while True:
        ret,img = cap.read()

        img = cv2.flip(img,1)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        result = hands.process(img)
        img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
        # 관절 벡터 구하기
        if result.multi_hand_landmarks is not None:
            for res in result.multi_hand_landmarks:
                joint = np.zeros((21,3))
                for j,lm in enumerate(res.landmark):
                    joint[j] = [lm.x,lm.y,lm.z]
                # 관절 벡터 가져 올 묶음 쌍
                v1 = joint[[0,1,2,3,0,5,6,7,0,9,10,11,0,13,14,15,0,17,18,19], :]
                v2 = joint[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], :]
                v = v2 - v1
                # 정규화
                v = v / np.linalg.norm(v,axis=1)[:,np.newaxis]

                angle = np.arccos( np.einsum('nt,nt->n',
                                             v[[0,1,2,4,5,6,8,9,10,12,13,14,16,17,18],:],
                                             v[[1,2,3,5,6,7,9,10,11,13,14,15,17,18,19],:]
                                             ) )

                angle = np.degrees(angle)
                data = np.array([angle],dtype=np.float32)
                data = np.append(data, 3)

                mp_drawing.draw_landmarks(img,res,mp_hands.HAND_CONNECTIONS)

        cv2.imshow('Dataset',img)
        if cv2.waitKey(1) == ord('q'):
            break
'''
einsum 하면 rad 값이 구해짐. 

아니면 각각의 벡터를 하나하나씩 반복문 돌려서 해 주어야 함.

키를 누를 때마다 학습 데이터 저장하기
'''
total_result = np.array(total_result,dtype=np.float32)
df = pd.DataFrame(total_result)
print(total_result)
df.to_csv('hand.csv',mode='a',index=None,header=None)
print('=========end==============')