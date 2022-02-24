from pyPAIX.nmc2_DIO import DIO
io = DIO()

def digitalRead(index):#index:1~16
    tot_hex = io.checkIn()
    data_ = []
    tot_bin = ""
    for i in range(1,16):
        data_.append(tot_hex[2*(i-1):2*i])
        tot_bin += control_digit(bin(int(data_[-1],16))[2:],8)[::-1]
    return tot_bin[index-1]

def control_digit(s_in,number):
    s_out = ""
    for i in range(number-len(s_in)):
        s_out += '0'
    s_out += s_in
    return s_out

def digitalWrite(index, value): #index:1~16, value:1/0
    io.write(index-1,value)

if __name__ == '__main__':
    print(digitalRead(15))
    print(digitalRead(16))
