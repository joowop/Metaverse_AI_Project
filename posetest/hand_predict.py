import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import socket

max_num_hands = 1
gesture = { 0:'stop' , 1:'fire' }

df = pd.read_csv('hand.csv',header=None)
x = df.iloc[:,:-1]
y = df.iloc[:,-1]
x = x.to_numpy().astype(np.float32)
y = y.to_numpy().astype(np.float32)

knn = cv2.ml.KNearest_create()
knn.train(x, cv2.ml.ROW_SAMPLE, y)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sendport = ('127.0.0.1',5053)

cap = cv2.VideoCapture(0)

total_result = []


with mp_hands.Hands(max_num_hands=max_num_hands, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while True:
        ret,img = cap.read()

        img = cv2.flip(img,1)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        result = hands.process(img)
        img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)

        if result.multi_hand_landmarks is not None:
            for res in result.multi_hand_landmarks:
                joint = np.zeros((21,3))
                for j,lm in enumerate(res.landmark):
                    joint[j] = [lm.x,lm.y,lm.z]

                v1 = joint[[0,1,2,3,0,5,6,7,0,9,10,11,0,13,14,15,0,17,18,19], :]
                v2 = joint[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], :]
                v = v2 - v1

                v = v / np.linalg.norm(v,axis=1)[:,np.newaxis]

                angle = np.arccos( np.einsum('nt,nt->n',
                                             v[[0,1,2,4,5,6,8,9,10,12,13,14,16,17,18],:],
                                             v[[1,2,3,5,6,7,9,10,11,13,14,15,17,18,19],:]
                                             ) )

                angle = np.degrees(angle)
                data = np.array([angle],dtype=np.float32)
                ret,rdata,neig,dist = knn.findNearest(data,5)
                idx = int(rdata[0][0])
                print(idx)
                senddata = str(idx)
                sock.sendto(str.encode(senddata), sendport)

                data = np.append(data,1)



                mp_drawing.draw_landmarks(img,res,mp_hands.HAND_CONNECTIONS)

        cv2.imshow('Dataset',img)
        if cv2.waitKey(1) == ord('q'):
            break