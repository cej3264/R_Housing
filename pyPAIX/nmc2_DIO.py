from threading import *
from socket import *
import time
import binascii

class DIO:

    def __init__(self, ip = '192.168.30.11', port=1000):
        self.bConnect = False
        self.idCode = 1
        self.msg = ""
        self.log = []
        self.digitalIn = []
        self.connect(ip , port)
        self.idCheck = True

    def __del__(self):
        self.stop()

    def connect(self, ip = '192.168.30.11', port=1000):
        self.client = socket(AF_INET, SOCK_STREAM)

        try:
            self.client.connect((ip, port))
        except Exception as e:
            print('Connect Error : ', e)
            return False
        else:
            self.bConnect = True
            self.t = Thread(target=self.receive, args=(self.client,))
            self.t.start()
            print('Connected')

        return True

    def stop(self):
        self.bConnect = False
        if hasattr(self, 'client'):
            self.client.close()
            del (self.client)
            print('Client Stop')

    def receive(self, client):
        while self.bConnect:
            try:
                recv = client.recv(1024)
            except Exception as e:
                print('Recv() Error :', e)
                break
            else:
                b_msg = self.a2h(recv)
                msg = str(b_msg, encoding='utf-8')
                if msg:
                    #print('[RECV]:', msg)
                    self.msg = msg
                    self.idCheck = self._idCode(msg)
                    for log in self.log:
                        if log[2] == b_msg[-4:]:
                            log.append(msg)
                    #print(self.log)
        self.stop()

    def _idCode(self, recv):
        r_idc = recv[:8]
        _idcode = r_idc[-2:] + r_idc[-4:-2] + r_idc[-6:-4] + r_idc[-8:-6]
        idcode = int(_idcode)
        #print(idcode)
        if idcode == self.idCode-1:
            return True
        else:
            return False

    def send(self, msg):
        if not self.bConnect:
            return

        try:
            self.client.send(msg)
            #print('[SEND]:', msg)
            self.idCode += 1
        except Exception as e:
            print('Send() Error : ', e)

    def checkSum(self, msg):
        nLen = len(msg)-1
        sum = 0
        for i in range(nLen):
            sum += msg[i]
        cksum1 = hex(sum)[3:].encode()
        cksum2 = b'0' + hex(sum)[2:3].encode()
        cksum = cksum1 + cksum2

        tmp = [self.idCode, msg, cksum]
        self.log.append(tmp)

        a_cksum = self.h2a(cksum)
        return a_cksum

    def a2h(self, a):
        h = binascii.b2a_hex(a)
        return h

    def h2a(self, h):
        a = binascii.a2b_hex(h)
        return a

    def makeCmd(self, cmd):
        b_id = str(self.idCode).encode()
        cmd = b_id + b" " + cmd
        is_odd = len(cmd) % 2
        cmd = cmd + b" " + (b'\n' * is_odd) + b'\n'
        checksum = self.checkSum(cmd)
        cmd = cmd + checksum
        return cmd

    def checkIn(self):
        cmd = b'INX'
        msg = self.makeCmd(cmd)
        self.send(msg)
        time.sleep(0.01)
        if self.idCheck:
            self.digitalIn = self.msg
        else:
            print('idCheck() Error')
        return self.digitalIn[12:-8]

    def checkOut(self):
        cmd = b'ISOUTX'
        msg = self.makeCmd(cmd)
        self.send(msg)

    def write(self, pinNum, status):
        b_pinNum = b'0' + hex(pinNum)[2:].encode()
        b_stat = str(status).encode()
        cmd = b'OUTXBIT ' + b_pinNum + b' ' + b_stat
        msg = self.makeCmd(cmd)
        self.send(msg)

    def toggle(self, pinNum):
        b_pinNum = b'0' + hex(pinNum)[2:].encode()
        cmd = b'OUTXTOG ' + b_pinNum
        msg = self.makeCmd(cmd)
        self.send(msg)

    def writeAll(self, pinList):
        print("will be added")

    def mWrite(self, pinList):
        print("will be added")

    def mToggle(self, pinList):
        print("will be added")

    def read(self, index):  # index:0~15
        index += 1
        tot_hex = self.checkIn()
        data_ = []
        tot_bin = ""
        for i in range(1, 16):
            data_.append(tot_hex[2 * (i - 1):2 * i])
            tot_bin += self.control_digit(bin(int(data_[-1], 16))[2:], 8)[::-1]
        return tot_bin[index - 1]

    def control_digit(self, s_in, number):
        s_out = ""
        for i in range(number - len(s_in)):
            s_out += '0'
        s_out += s_in
        return s_out
