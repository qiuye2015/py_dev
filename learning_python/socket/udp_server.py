# -*- coding: utf-8 -*-

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # 使用UDP协议
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 56788))

while True:
    data = sock.recv(1024)
    if data == b'quit' or data == b'exit':
        print('再见')
        break
    else:
        print(data)


