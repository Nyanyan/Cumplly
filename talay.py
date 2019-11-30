import serial
import serial.tools.list_ports
import os

def search_com_port():
    coms = serial.tools.list_ports.comports()
    comlist = []
    for com in coms:
        comlist.append(com.device)
    print('Connected COM ports: ' + str(comlist))
    use_port = comlist[0]
    print('Use COM port: ' + use_port)
    return use_port

port = search_com_port()


num = 0
while True:
    ser = serial.Serial()
    ser.port = port
    ser.baundrate = 9600
    ser.timeout = 0.1 #sec
    ser.setDTR(False)
    ser.open()

    line = ser.readline()
    line = line.decode().rstrip(os.linesep)
    if line != '':
        print(line)
        f = True
        arr = ['0','1','2','3','4','5','6','7','8','9']
        if line[0] in arr:
            if len(line) == 10:
                checksum = 64
                for j in range(6):
                    checksum += int(line[j + 3])
                if chr(checksum) == line[9]:
                    f = True
                    num = int(line[0])
                    minute = int(line[3])
                    second = int(line[4]) * 10 + int(line[5])
                    msecond = int(line[6]) * 100 + int(line[7]) * 10 + int(line[8])
                    print(num,minute,second,msecond)
                else:
                    f = False
        if f == True:
            ser.write('y'.encode())
        else:
            ser.write('n'.encode())
    
    ser.close()
