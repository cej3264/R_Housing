class Optifunction:

    def home(self):
        txt = "home()"
        self.client_socket.send(txt.encode('utf-8'))

    def movej(self, j1, j2, j3, j4, j5, j6):
        txt = "movej(" + j1 + ", " + j2 + ", " + j3 + ", " + j4 + ", " + j5 + ", " + j6 + ")"
        self.client_socket.send(txt.encode('utf-8'))

    def movel(self, x, y, z, yaw, pitch, roll):
        txt = "movel(" + x + ", " + y + ", " + z + ", " + yaw + ", " + pitch + ", " + roll + ")"
        self.client_socket.send(txt.encode('utf-8'))

    def stop(self):
        txt = "stop()"
        self.client_socket.send(txt.encode('utf-8'))

    def stay(self):
        txt = "stay()"
        self.client_socket.send(txt.encode('utf-8'))

    def gOpen(self):
        txt = "gOpen()"
        self.client_socket.send(txt.encode('utf-8'))

    def gClose(self):
        txt = "gClose()"
        self.client_socket.send(txt.encode('utf-8'))

    def set_prof(self, spd, acc):
        self.spd = spd
        self.acc = acc

        txt = "set_prof(" + str(self.spd) + ", " + str(self.acc) + ")"
        self.client_socket.send(txt.encode('utf-8'))

    def currAngles(self):
        txt = "currAngles()"
        self.client_socket.send(txt.encode('utf-8'))

        try:
            recv = self.client_socket.recv(1024)
        except Exception as e:
            print('Recv() Error :', e)
        else:
            msg = str(recv, encoding='utf-8')
            if msg:
               self.angles = msg.split(' ')

        return self.angles

    def currLocation(self):
        txt = "currLocation()"
        self.client_socket.send(txt.encode('utf-8'))

        try:
            recv = self.client_socket.recv(1024)
        except Exception as e:
            print('Recv() Error :', e)
        else:
            msg = str(recv, encoding='utf-8')
            if msg:
               self.location = msg.split(' ')

        return self.location

    def currGripper(self):
        txt = "currGripper()"
        self.client_socket.send(txt.encode('utf-8'))

        try:
            recv = self.client_socket.recv(1024)
        except Exception as e:
            print('Recv() Error :', e)
        else:
            msg = str(recv, encoding='utf-8')

        return msg