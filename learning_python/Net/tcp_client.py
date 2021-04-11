import socket

def main():
    #创建udp套接字
    #udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # TCP连接服务器
    dest_addr = ("127.0.0.1",8888)
    tcp_socket.connect(dest_addr)
    
    while True:
        send_data = input("please Input string:")
        if send_data == "exit":
            break

        #使用套接字收发数据
        tcp_socket.send(send_data.encode("utf-8"))


    #关闭套接字
    tcp_socket.close()
    print("---------run---------")

if __name__ == "__main__":
    main()
