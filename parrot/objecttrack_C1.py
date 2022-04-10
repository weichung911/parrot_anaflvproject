import time
import numpy as np
from PIL import ImageGrab
import cv2
from socket import AF_INET, socket, SOCK_STREAM
import socket
from threading import Thread
import tkinter

def boundingRect(h,w,cnt):
    top = h
    down = 0
    left = w
    right = 0
    for i in range(len(cnt)):
        if(top > cnt[i][0]):
            top = cnt[i][0]
        if(down < cnt[i][0]):
            down =cnt[i][0]
        if(left > cnt[i][1]):
            left = cnt[i][1]
        if(right < cnt[i][1]):
            right =cnt[i][1]
    h = down - top;
    w = right - left;
    y = top
    x = left

    return x,y,w,h

def getcolor(image):
    height,width = image.shape[:2]

    lower_red = np.array([160, 60, 60])
    upper_red = np.array([180, 255, 255])

    lower_red2 = np.array([70, 87, 0])
    upper_red2 = np.array([179, 255, 255])  # thers is two ranges of red


    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # cv2.imshow('123',hsv)
    mask_r = cv2.inRange(hsv, lower_red, upper_red)

    mask_r2 = cv2.inRange(hsv, lower_red2, upper_red2)

    mask = mask_r + mask_r2

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.dilate(mask, kernel,iterations = 10)

    mask = cv2.erode(mask, kernel, iterations = 3)

    ret, thresh = cv2.threshold(mask, 150, 255, 0)
    # 尋找輪廓
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    cont = contours[0]

    # print(mask)
    x_left,y_up,w1,h1 = cv2.boundingRect(cont)
    y_down = h1 + y_up
    x_right = x_left + w1
    # print(x_left,x_left,y_up,y_down)
    cv2.rectangle(hsv, (x_left, y_up), (x_left + w1, y_up + h1), (0, 255, 0), 2)
    # cv2.imshow('123',hsv)
    # height,width = image.shape[:2]
    red = np.array([55,5,20])
    color_range = np.array([30,30,30])
    img2 = image

    cv2.rectangle(img2, (x_left, y_up), (x_left + w1, y_up + h1), (0, 255, 0), 2)
    # cv2.imshow('123',img2)
    c = 0
    m = 0
    S_range = 5
    #
    for x in range(x_left,x_right,3):
        for y in range(y_up,y_down,3):
            temp = image[y,x,:]
            if (all(red + color_range > image[y,x,:]) & all(image[y,x,:]> red - color_range)):
                img2[y,x,:] = [255,0,0]
                if (c == 0):
                    # cnt = [[y,x]]
                    c = 1
                    m = 1
                # else:
                    # cnt.append([y,x])

    # print(cnt[0])
    cv2.rectangle(img2, (200, 104), (200 + 10, 104 + (2*S_range)), (0, 0, 255), 1)

    if (m == 1):
        # x, y, w, h = boundingRect(height,width,cnt)
        # cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 255, 0), 2)
        post = [round(x_left + (w1/2)), round(y_up +h1/2)]
        if(((post[0]>(205 - S_range))&(post[0]<(205 + S_range)))&((post[1]>(109 - S_range))&((post[1]<109 + S_range)))):
            cv2.rectangle(img2, (200, 104), (200 + 10, 104 + (2*S_range)), (255, 0, 0), 1)
        else:
            cv2.rectangle(img2, (200, 104), (200 + 10, 104 + (2*S_range)), (0, 0, 255), 1)

        img2[post[1],post[0],:] = [0,255,0]
    else:
        post = [-1,-1]
    img2 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    return img2 ,post

def screen():
    img = ImageGrab.grab(bbox=(70, 70, 910, 525))
    img = np.array(img)
    # BGR = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    imS = cv2.resize(img, (420, 228))
    imc , post = getcolor(imS)
    post = [2*post[0], 2*post[1]]
    return imc ,post



i = 0
m0 = 0
HOST = '127.0.0.1'
PORT = 3300

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

while(i == 0):


#     # img , post= screen()
#     #
#     # cv2.imshow('frame', img)
#     # print(post)
#
    serverMessage = client.recv(1024)
    serverMessage = str(serverMessage)
    print((serverMessage))
    if serverMessage == "b'OK'" :

        img , post= screen()

        cv2.imshow('frame', img)
        print(post)


        clientMessage = str(post)
        print(clientMessage)

        # # Convert To String
        # clientMessage = str(clientMessage)
        # # Encode String
        # clientMessage = clientMessage.encode()
        # # Send Encoded String version of the List
        client.send(clientMessage.encode())
        print(clientMessage)
#         time.sleep(0.5)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
