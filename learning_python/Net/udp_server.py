import socket

def main():
    udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    local_addr = ("",8888)
    udp_socket.bind(local_addr)

    while True:
        recv_data = udp_socket.recvfrom(1024)
        # recv_data(接收到的数据，（发送方的ip,port）)
        recv_msg = recv_data[0]
        recv_addr = recv_data[1]
        print("%s-->%s" % (str(recv_addr),recv_msg.decode("utf-8")))

    udp_socket.close()

if __name__ == "__main__":
    main()
