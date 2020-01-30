#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import socket
import _thread
import sys,time
import websocket
from bottle import get,post,run,request,template

CONTROL_IP='47.95.237.122'
CONTROL_PORT=10437

################################################

def heartbeat(conn, addr):
    print('heartbeat start.')
    while True:
        msg = conn.send('heartbeat'.encode())
        time.sleep(0.1)
    conn.close()
    print('heartbeat exit.')


def control(conn, addr):
    print('control start.')
    while True:
        msg = conn.recv(1024)
        if not msg:
            break
        print(addr, 'said: ', msg)
    conn.close()
    print('control exit.')


def server_program(control_ip, control_port):
    #host = socket.gethostname()
    host = control_ip
    port = control_port

    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.connect((host, port))
    _thread.start_new_thread(heartbeat, (server_socket, host,))
    _thread.start_new_thread(control, (server_socket, host,))

################################################

server_program(CONTROL_IP, CONTROL_PORT)
while True:
    time.sleep(1)


