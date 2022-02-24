import serial
import time

class controller:
    def __init__ (self, port, baudrate = 38400, parity = serial.PARITY_ODD, stopbits = serial.STOPBITS_ONE, databit = serial.EIGHTBITS, node = 1):
        self.pos = 0 # position
        self.pt = '' # current point number
        self.spd = 0.0 # current spped
        self.tem = 0 # temperature
        self.l_r = 0 # load rate
        self.o_s = 0 # operation status
        self.move_rsp = '' 
        self.action_rsp = ''
        self.stop_rsp = ''
        self.is_busy = 0
        self.robot = []

        try:
            self.robot = serial.Serial(
                port,
                baudrate,
                databit,
                parity,
                stopbits
            )
        except TypeError as e:
            print("Serial Error: ", e)
            self.robot.close()
            return None

        else:
            self.is_busy = 1
            cmd = b'@RESET.' + str(node).encode('utf-8') + b'\r\n'
            self.robot.write(cmd)
            tmp = self.robot.read_until(b'\n').decode('utf-8')
            print(tmp)
            if tmp[0:2] != "OK":
                return None

            time.sleep(1)

            cmd = b'@SRVO1.' + str(node).encode('utf-8') + b'\r\n'
            self.robot.write(cmd)
            tmp = self.robot.read_until(b'\n').decode('utf-8')
            print(tmp)
            if tmp[0:2] != "OK":
                return None

            time.sleep(1)

            cmd = b'@ORG.' + str(node).encode('utf-8') + b'\r\n'
            self.robot.write(cmd)
            tmp = self.robot.read_until(b'\n').decode('utf-8')
            print(tmp)
            tmp = self.robot.read_until(b'\n').decode('utf-8')
            print(tmp)

            self.is_busy = 0

            #time.sleep(0.5)
            #self.status()


    def move(self, point, node = 1):
        try:
            self.is_busy = 1
            cmd = b'@START' + point.encode('utf-8') + b'.' + str(node).encode('utf-8') + b'\r\n'
            self.robot.write(cmd)
        except:
            print("move error")
            return False
        else:
            while True:
                self.move_rsp = self.robot.read_until(b'\n').decode('utf-8')
                print(self.move_rsp)
                if self.move_rsp.find('END') >= 0:
                    print("break")
                    break

            self.is_busy = 0
            #time.sleep(0.3)
            #self.status()
            return True

    def stop(self, node=1):
        try:
            cmd = b'@STOP.' +  str(node).encode('utf-8') + b'\r\n'
            self.robot.write(cmd)
        except:
            print("stop error")
            return False
        else:
            self.move_rsp = self.robot.read_until(b'\n').decode('utf-8')

            #self.status()
            return True



    def status(self, node = 1):
        # pos
        try:
            cmd = b'@?D0.' + str(node).encode('utf-8') + b'\r\n'
            self.robot.write(cmd)
            tmp = self.robot.read_until(b'\n').decode('utf-8')
            self.pos = int(tmp[tmp.find("=")+1:tmp.find(" ")-1])
            tmp = self.robot.read_until(b'\n').decode('utf-8')
        except:
            print("read pos error")
            return False

        #point_number
        try:
            cmd = b'@?D13.' + str(node).encode('utf-8') + b'\r\n'
            self.robot.write(cmd)
            tmp = self.robot.read_until(b'\n').decode('utf-8')
            self.pt = tmp[tmp.find("=") + 1:tmp.find(" ")-1]
            tmp = self.robot.read_until(b'\n').decode('utf-8')
        except:
            print("read point error")
            return False

        #spd
        try:
            cmd = b'@?D1.' + str(node).encode('utf-8') + b'\r\n'
            self.robot.write(cmd)
            tmp = self.robot.read_until(b'\n').decode('utf-8')
            self.spd = float(tmp[tmp.find("=") + 1:tmp.find(" ") - 1])
            #print("spd",tmp)
            tmp = self.robot.read_until(b'\n').decode('utf-8')
        except:
            print("read speed error")
            return False

        #tem
        try:
            cmd = b'@?D10.' + str(node).encode('utf-8') + b'\r\n'
            self.robot.write(cmd)
            tmp = self.robot.read_until(b'\n').decode('utf-8')
            #print("tem", tmp)
            self.tem = int(tmp[tmp.find("=") + 1:tmp.find(" ") - 1])
            tmp = self.robot.read_until(b'\n').decode('utf-8')
        except:
            print("read tem error")
            return False

        #L_r
        try:
            cmd = b'@?D14.' + str(node).encode('utf-8') + b'\r\n'
            self.robot.write(cmd)
            tmp = self.robot.read_until(b'\n').decode('utf-8')
            self.l_r = int(tmp[tmp.find("=") + 1:tmp.find(" ") - 1])
            tmp = self.robot.read_until(b'\n').decode('utf-8')
        except:
            print("read load error")
            return False

        #O_s
        try:
            cmd = b'@?D18.' + str(node).encode('utf-8') + b'\r\n'
            self.robot.write(cmd)
            tmp = self.robot.read_until(b'\n').decode('utf-8')
            self.o_s = int(tmp[tmp.find("=") + 1:tmp.find(" ") - 1])
            tmp = self.robot.read_until(b'\n').decode('utf-8')
        except:
            print("read status error")
            return False

        return True

    def action(self, msg):
        cmd = msg.encode('utf-8')
        try:
            self.robot.write(cmd)
        except:
            print("read error")
            return False
        else:
            self.action_rsp = self.robot.read_until(b'\n').decode('utf-8')
            self.action_rsp = self.robot.read_until(b'\n').decode('utf-8')
        return True


    def close(self):
        self.robot.close()
