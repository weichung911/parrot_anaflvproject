#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import socket

import olympe
import subprocess
import time
from olympe.messages.ardrone3.Piloting import TakeOff, Landing, PCMD
from olympe.messages.gimbal import set_target
from pynput.keyboard import Listener, Key, KeyCode
from collections import defaultdict
from enum import Enum

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("OK", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'OK'
    client.send(bytes(welcome, "utf8"))
    # print("11111")
    # msg = "%s has joined the chat!" % name
    # broadcast(bytes(msg, "utf8"))
    # clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        data = msg.decode('utf-8')

        data = data[1:-1].split(',')
        x = int(data[0])
        y = int(data[1])
        print(x,y)
        if ((x > 0) & (y >0)):
            # time.sleep(0.05)
            if(x > 400):
                roll = 1
            elif(x < 428):
                roll = -1
            else:
                roll = 0
            if(y < 208):
                throttle = 1
            elif(y > 228):
                throttle = -1
            else:
                throttle = 0

            print(roll,throttle)

            drone(PCMD(1,
                               roll,#control.roll(), #-100,0,100 # 左右平移
                               0,#control.pitch(),#-100,0,100# 前進後退
                               0,#control.yaw(),#-100,0,100# 左右旋轉
                               throttle,#control.throttle(),#-100,0,100# 上升下降
                               timestampAndSeqNum=0,
                         ))
            drone(set_target(gimbal_id = 0,
              control_mode = "position",
              yaw_frame_of_reference = "relative",
                      yaw = 0,#control.camera_yaw(),#-100,0,100# 鏡頭左右旋
                      pitch_frame_of_reference = "relative",
                      pitch = 0,#control.camera_pitch(),#-100,0,100# 鏡頭俯仰
                      roll_frame_of_reference = "relative",
                      roll = 0 #control.camera_roll()#-100,0,100# 鏡頭左右移
                     )).wait
            time.sleep(0.05)
        client.send(bytes(welcome, "utf8"))
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)


clients = {}
addresses = {}
DRONE_IP = "192.168.42.1"
HOST = '127.0.0.1'
PORT = 3300
BUFSIZ = 1024
ADDR = (HOST, PORT)
drone = olympe.Drone(DRONE_IP)
drone.connection()
drone(TakeOff()).wait().success()
time.sleep(1)
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDR)
if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()


