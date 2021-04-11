# -*- coding: utf-8 -*-

import sys
import socketserver
from poetries import POUETRIES # 此处导入诗词库（poetries.py）

class PouetryTCPHandler(socketserver.StreamRequestHandler):
    """定义响应并处理Socket连接请求的类"""
    
    def handle(self):
        """业务处理"""
        
        print('%s:%d来了'%self.client_address)
        
        delay = 0.1 # 诗词显示速度（字间隔时间）
        subjects = [item.split()[0] for item in POUETRIES] # 诗词目录
        
        welcome = '欢迎来到风花雪月古诗词库！诗词目录如下：\r\n'
        welcome += '----------------------------------------\r\n'
        for index, subject in enumerate(subjects):
            welcome += '%d %s\r\n'%(index+1, subject)
        welcome += 'over\r\n' # 此处及他处，约定以独占一行的over作为服务端发送信息结束的标志
        welcome = welcome.encode('gbk')
        self.request.sendall(welcome) # 发送欢迎信息和诗词目录
        
        while True:
            cmd = self.rfile.readline().strip()
            if cmd == b'bye':
                print('%s:%d走了'%self.client_address)
                self.request.sendall(b'over\r\n')
                self.request.close()
                break
            elif cmd == b'help':
                self.request.sendall(welcome)
            elif cmd.isdigit():
                try:
                    index = int(cmd) - 1
                    assert -1 < index < len(POUETRIES)
                except:
                    self.request.sendall('无效的诗词序号\r\n'.encode('gbk'))
                    self.request.sendall(b'over\r\n')
                    continue
                
                self.request.sendall(POUETRIES[index].encode('gbk') + b'\r\n')
                self.request.sendall(b'over\r\n')
            else:
                self.request.sendall('无效的命令\r\n'.encode('gbk'))
                self.request.sendall(b'over\r\n')

def poetries_server(port, use_threading):
    """古诗词服务器"""
    
    if use_threading:
        #server = socketserver.ThreadedTCPServer(('127.0.0.1', port), PouetryTCPHandler) # 多线程服务
        server = socketserver.ThreadingTCPServer(('127.0.0.1', port), PouetryTCPHandler) # 多线程服务
    else:
        server = socketserver.TCPServer(('127.0.0.1', port), PouetryTCPHandler) # 单线程服务
    server.serve_forever()
    

if __name__ == '__main__':
    if len(sys.argv) == 1:
        port, use_threading = 56789, True
    elif  len(sys.argv) == 2:
        port, use_threading = int(sys.argv[1]), True
    elif  len(sys.argv) == 3:
        port, use_threading = int(sys.argv[1]), bool(int(sys.argv[2]))
    
    poetries_server(port, use_threading)
    