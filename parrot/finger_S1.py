#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
import socket
from threading import Thread
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
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        data = msg.decode('utf-8')
        if data != bytes("{quit}", "utf8"):
            print(data)
            if data == '1':
                print("one")
                for i in range(0,25):
                    drone(PCMD(1,
                                       0,#control.roll(), #-100,0,100 # 左右平移
                                       0,#control.pitch(),#-100,0,100# 前進後退
                                       0,#control.yaw(),#-100,0,100# 左右旋轉
                                       0,#control.throttle(),#-100,0,100# 上升下降
                                       timestampAndSeqNum=0,
                                 ))
                    drone(set_target(gimbal_id = 0,
                      control_mode = "position",
                      yaw_frame_of_reference = "relative",
                              yaw = 0,#control.camera_yaw(),#-100,0,100# 鏡頭左右旋
                              pitch_frame_of_reference = "relative",
                              pitch = 0,#control.camera_pitch(),#-100,0,100# 鏡頭俯仰
                              roll_frame_of_reference = "relative",
                              roll = 100 #control.camera_roll()#-100,0,100# 鏡頭左右移
                             )).wait
                    time.sleep(0.035)
                for i in range(0,25):
                    drone(PCMD(1,
                                       0,#control.roll(), #-100,0,100 # 左右平移
                                       0,#control.pitch(),#-100,0,100# 前進後退
                                       0,#control.yaw(),#-100,0,100# 左右旋轉
                                       0,#control.throttle(),#-100,0,100# 上升下降
                                       timestampAndSeqNum=0,
                                 ))
                    drone(set_target(gimbal_id = 0,
                      control_mode = "position",
                      yaw_frame_of_reference = "relative",
                              yaw = -100,#control.camera_yaw(),#-100,0,100# 鏡頭左右旋
                              pitch_frame_of_reference = "relative",
                              pitch = 0,#control.camera_pitch(),#-100,0,100# 鏡頭俯仰
                              roll_frame_of_reference = "relative",
                              roll = 0 #control.camera_roll()#-100,0,100# 鏡頭左右移
                             )).wait
                    time.sleep(0.035)
            if data == '2':
                print("two")
                for i in range(0,25):
                    drone(PCMD(1,
                                       0,#control.roll(), #-100,0,100 # 左右平移
                                       0,#control.pitch(),#-100,0,100# 前進後退
                                       0,#control.yaw(),#-100,0,100# 左右旋轉
                                       0,#control.throttle(),#-100,0,100# 上升下降
                                       timestampAndSeqNum=0,
                                 ))
                    drone(set_target(gimbal_id = 0,
                      control_mode = "position",
                      yaw_frame_of_reference = "relative",
                              yaw = 0,#control.camera_yaw(),#-100,0,100# 鏡頭左右旋
                              pitch_frame_of_reference = "relative",
                              pitch = 0,#control.camera_pitch(),#-100,0,100# 鏡頭俯仰
                              roll_frame_of_reference = "relative",
                              roll = -100 #control.camera_roll()#-100,0,100# 鏡頭左右移
                             )).wait
                    time.sleep(0.035)
                for i in range(0,25):
                    drone(PCMD(1,
                                       0,#control.roll(), #-100,0,100 # 左右平移
                                       0,#control.pitch(),#-100,0,100# 前進後退
                                       0,#control.yaw(),#-100,0,100# 左右旋轉
                                       0,#control.throttle(),#-100,0,100# 上升下降
                                       timestampAndSeqNum=0,
                                 ))
                    drone(set_target(gimbal_id = 0,
                      control_mode = "position",
                      yaw_frame_of_reference = "relative",
                              yaw = 100,#control.camera_yaw(),#-100,0,100# 鏡頭左右旋
                              pitch_frame_of_reference = "relative",
                              pitch = 0,#control.camera_pitch(),#-100,0,100# 鏡頭俯仰
                              roll_frame_of_reference = "relative",
                              roll = 0 #control.camera_roll()#-100,0,100# 鏡頭左右移
                             )).wait
                    time.sleep(0.035)
            if data == '3':
                print("three")
                # with olympe.Drone(DRONE_IP) as drone:
                #     for i in range(0,25):
                #         drone(PCMD(1,
                #                            0,#control.roll(), #-100,0,100 # 左右平移
                #                            0,#control.pitch(),#-100,0,100# 前進後退
                #                            0,#control.yaw(),#-100,0,100# 左右旋轉
                #                            0,#control.throttle(),#-100,0,100# 上升下降
                #                            timestampAndSeqNum=0,
                #                      ))
                #         drone(set_target(gimbal_id = 0,
                #           control_mode = "position",
                #           yaw_frame_of_reference = "relative",
                #                   yaw = 10,#control.camera_yaw(),#-100,0,100# 鏡頭左右旋
                #                   pitch_frame_of_reference = "relative",
                #                   pitch = 0,#control.camera_pitch(),#-100,0,100# 鏡頭俯仰
                #                   roll_frame_of_reference = "relative",
                #                   roll = 0 #control.camera_roll()#-100,0,100# 鏡頭左右移
                #                  )).wait
                #         time.sleep(0.05)
            if data == '4':
                print("four")
                assert drone(Landing()).wait().success()
                # with olympe.Drone(DRONE_IP) as drone:
                #     for i in range(0,25):
                #         drone(PCMD(1,
                #                            0,#control.roll(), #-100,0,100 # 左右平移
                #                            0,#control.pitch(),#-100,0,100# 前進後退
                #                            0,#control.yaw(),#-100,0,100# 左右旋轉
                #                            0,#control.throttle(),#-100,0,100# 上升下降
                #                            timestampAndSeqNum=0,
                #                      ))
                #         drone(set_target(gimbal_id = 0,
                #           control_mode = "position",
                #           yaw_frame_of_reference = "relative",
                #                   yaw = -10,#control.camera_yaw(),#-100,0,100# 鏡頭左右旋
                #                   pitch_frame_of_reference = "relative",
                #                   pitch = 0,#control.camera_pitch(),#-100,0,100# 鏡頭俯仰
                #                   roll_frame_of_reference = "relative",
                #                   roll = 0 #control.camera_roll()#-100,0,100# 鏡頭左右移
                #                  )).wait
                #         time.sleep(0.05)
            if data == '5':
                print("five")
                # with olympe.Drone(DRONE_IP) as drone:
                #     drone(Landing()).wait().success()

            client.send(bytes(welcome, "utf8"))

def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)


clients = {}
addresses = {}
DRONE_IP = "192.168.42.1"
HOST = '127.0.0.1'
PORT = 1234
BUFSIZ = 1024
ADDR = (HOST, PORT)
drone = olympe.Drone(DRONE_IP)
drone.connection()
drone(TakeOff()).wait().success()
for i in range(0,3):
                    drone(PCMD(1,
                                       0,#control.roll(), #-100,0,100 # 左右平移
                                       0,#control.pitch(),#-100,0,100# 前進後退
                                       0,#control.yaw(),#-100,0,100# 左右旋轉
                                       12,#control.throttle(),#-100,0,100# 上升下降
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
                    time.sleep(1)
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
