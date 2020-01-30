#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import socket
import _thread
import sys,time
import websocket
from bottle import get,post,run,request,template

CONTROL_PORT=10437
HTML_PORT=10247
CONTROL_CMDS=['left', 'right', 'front', 'rear']
control_cmd = 'stop'

@get("/")
def index():
    return template("index.html")

@post("/buttondown")
def handle_button_down():
    global control_cmd
    key = request.body.read().decode()
    if key in CONTROL_CMDS:
        control_cmd = key

@post("/buttonup")
def handle_button_up():
    global control_cmd
    key = request.body.read().decode()
    if key in CONTROL_CMDS:
        control_cmd = 'stop'

################################################

def heartbeat(conn, addr):
    print('heartbeat start.')
    while True:
        msg = conn.recv(1024)
        if not msg:
            break
        print(addr, 'said: ', msg)
    conn.close()
    print('heartbeat exit.')

def on_new_client(conn, addr):
    global control_cmd
    print("client: " + str(addr))
    _thread.start_new_thread(heartbeat, (conn, addr,))

    while True:
        try:
            msg = control_cmd.encode()
            print('send: ', msg)
            l = conn.send(msg)
            time.sleep(0.1)
        except Exception as e:
            print(e)
            break
    print('client exit!')

def server_program(control_port):
    host = socket.gethostname()
    port = control_port

    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))

    server_socket.listen(1)
    while True:
        conn, address = server_socket.accept()
        _thread.start_new_thread(on_new_client, (conn, address,) )

################################################

_thread.start_new_thread(server_program, (CONTROL_PORT,))
run(host="0.0.0.0", port=HTML_PORT)

