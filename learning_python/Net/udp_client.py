import socket

def main():
    #创建udp套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("",6666))
    dest_addr = ("127.0.0.1",8888)

    while True:
        send_data = input("please Input string:")
        if send_data == "exit":
            break

        #使用套接字收发数据
        #udp_socket.sendto(b"",dest_addr)
        udp_socket.sendto(send_data.encode("utf-8"),dest_addr)


    #关闭套接字
    udp_socket.close()
    print("---------run---------")

if __name__ == "__main__":
    main()
