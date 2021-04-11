import socket

def main():
    #udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    # 监听套接字
    tcp_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcp_socket.bind(("",8888))
    tcp_socket.listen(128)

    while True:
        print("wating...")
        # 服务套接字
        client_socket,client_addr = tcp_socket.accept()
        print("%s已连接" % str(client_addr))

        while True:
            recv_data = client_socket.recv(1024)
            # 如果recv解阻塞
            # 1，接收到数据
            # 2. 客户端调用close
            if recv_data:
                print("接收数据为：%s" % recv_data.decode("utf-8"))
            else:
                break

        client_socket.close()

    tcp_socket.close()


if __name__ == "__main__":
    main()
