# -*- coding: utf-8 -*-

import socket

def send_message_by_udp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # 使用UDP协议
    while True:
        msg = input('请输入要发送的信息：').strip()
        sock.sendto(msg.encode('gbk'), ('127.0.0.1', 56788))
        if msg == 'quit' or msg == 'exit':
            break

send_message_by_udp()
