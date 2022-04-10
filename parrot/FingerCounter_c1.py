import cv2
import time
import os
import HandTrackingModule as htm
import numpy as np
from PIL import ImageGrab
import cv2
import socket
import time

# folderPath = "FingerImages"
# myList = os.listdir(folderPath)
# print(myList)
# overlayList = []
# for imPath in myList:
#     image = cv2.imread(f'{folderPath}/{imPath}')
#     # print(f'{folderPath}/{imPath}')
#     overlayList.append(image)
flag = 0
flag_m = 0
atime = time.time()
btime = time.time()
def localtime( img):
    seconds = time.time()
    local_time = time.ctime(seconds)
    cv2.imwrite('finger_img/' + str(local_time) +'.jpg', img)



# print(len(overlayList))
pTime = 0

detector = htm.handDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]
#
HOST = '127.0.0.1'
PORT = 1234

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# flag = 0

while True:
    img = ImageGrab.grab(bbox=(70, 70, 910, 525))
    img = np.array(img)
    BGR = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imS = cv2.resize(BGR, (640, 480))
    img = detector.findHands(imS)
    lmList = detector.findPosition(img, draw=False)
    totalFingers = 0
    # print(lmList)

    if len(lmList) != 0:
        fingers = []

        # Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 Fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # print(fingers)
        totalFingers = fingers.count(1)
        print(totalFingers)


        # cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                    10, (255, 0, 0), 25)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    ntime = time.time()
    flag = 0 if ntime - atime > 5 else 1
    flag_m = 1 if ntime - btime > 2 else 0
    # serverMessage = client.recv(1024)
    # serverMessage = str(serverMessage)
    # print((serverMessage))
    # print(flag_m)
    # print(ntime-btime)
    if flag_m :
        btime = time.time()
        flag_m = 0
        serverMessage = client.recv(1024)
        serverMessage = str(serverMessage)
        print((serverMessage))
        if serverMessage == "b'OK'" :
            clientMessage = str(totalFingers)
            print(clientMessage)
            # # Convert To String
            # clientMessage = str(clientMessage)
            # # Encode String
            # clientMessage = clientMessage.encode()
            # # Send Encoded String version of the List
            # print(flag_m)
            client.send(clientMessage.encode())
            if clientMessage == '3':
                if flag == 0:
                    localtime(img)
                    flag = 1
                    atime = time.time()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
