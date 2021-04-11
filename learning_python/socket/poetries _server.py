# -*- coding: utf-8 -*-

import sys, time
import socketserver
from poetries import POUETRIES # 此处导入诗词库（poetries.py）

class PouetryTCPHandler(socketserver.StreamRequestHandler):
    """定义响应并处理Socket连接请求的类"""
    
    def handle(self):
        """业务处理"""
        
        delay = 0.1 # 诗词显示速度（字间隔时间）
        subjects = [item.split()[0] for item in POUETRIES] # 诗词目录
        welcome = '欢迎来到风花雪月古诗词库, 请输入序号后回车以选择你喜欢的诗词\r\n'
        welcome += '输入fast加速，输入slow减速，输入bye退出\r\n\r\n'
        for index, subject in enumerate(subjects):
            welcome += '%d %s\r\n'%(index+1, subject)
        welcome += '\r\n'
        welcome = welcome.encode('gbk')
        self.request.sendall(welcome) # 发送欢迎信息和诗词目录
        self.request.sendall(b'')
        
        while True:
            cmd = self.rfile.readline().strip()
            if cmd == b'bye':
                self.request.sendall('再见\r\n'.encode('gbk'))
                self.request.close()
                break
            elif cmd == b'help':
                self.request.sendall(welcome)
            elif cmd == b'fast':
                delay /= 2
                self.request.sendall('加速设置已完成\r\n'.encode('gbk'))
                self.request.sendall('请选择诗词序号，输入help显示诗词目录：\r\n\r\n'.encode('gbk'))
            elif cmd == b'slow':
                delay *= 2
                self.request.sendall('减速设置已完成\r\n'.encode('gbk'))
                self.request.sendall('请选择诗词序号，输入help显示诗词目录：\r\n\r\n'.encode('gbk'))
            else:
                try:
                    index = int(cmd) - 1
                    assert -1 < index < len(POUETRIES)
                except:
                    self.request.sendall('请输入有效的诗词序号，输入help显示诗词目录：\r\n\r\n'.encode('gbk'))
                    continue
                
                self.request.sendall(b'--------------------------\r\n')
                for line in POUETRIES[index].split('\n'):
                    for word in line:
                        self.request.sendall(word.encode('gbk'))
                        time.sleep(delay)
                    self.request.sendall(b'\r\n')
                self.request.sendall(b'--------------------------\r\n')
                self.request.sendall('请选择诗词序号，输入help显示诗词目录：\r\n\r\n'.encode('gbk'))

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
    