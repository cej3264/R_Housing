from Opti05Function import *
import socket

class Socket_connect_timeout(Exception):
    pass

class OptiConnector(Optifunction):

    def __init__(self):
        self.HOST = "192.168.30.100"
        self.PORT = 500
        self.state = False

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # WinError 10048 에러 해결를 위해 필요합니다.
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen()
        try:
            self.client_socket, self.addr = self.server_socket.accept()
             # 접속한 클라이언트의 주소입니다.
            print('Connected by', self.addr)
            self.state = True
        except Socket_connect_timeout as e:
            print(e)

    def close(self):    # 소켓을 닫습니다.
        self.client_socket.close()
        self.server_socket.close()
