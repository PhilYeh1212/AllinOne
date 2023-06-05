import csv
import time
import struct
import socket
from threading import Thread
from abc import ABC, abstractmethod

today = time.strftime('%y_%m_%d', time.localtime())

pathtoday = str('ModbusTCP_log_' + today + '.csv')
#print(file)
file = str(today + '_buffer for 10.csv')
path = r"C:\_Phil\02_Project\_ChenyaPVQA\data\23_05_27_buffer for 10.csv"
#path = r'C:\_Phil\DDS Data\21_12_22_buffer for 10'
#print(path)
DevID = '01'
FUNC = '03'
datalens = '3c'

# 觀察者接口
class Observer(ABC):
    @abstractmethod
    def update(self, data):
        pass

# 具體的觀察者 - 控制台打印觀察者
class ConsolePrintObserver(Observer):
    def update(self, data):
        print("Received data:", data)

# 主題類別
class Subject:
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    def notify(self, data):
        for observer in self.observers:
            observer.update(data)

# Modbus TCP Slave 單例類別
class ModbusTCPSlave:
    __instance = None

    @staticmethod
    def getInstance():
        if ModbusTCPSlave.__instance is None:
            ModbusTCPSlave()
        return ModbusTCPSlave.__instance

    def __init__(self):
        if ModbusTCPSlave.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ModbusTCPSlave.__instance = self
            self.subject = Subject()
            self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    def notify(self, data):
        for observer in self.observers:
            observer.update(data)

    def start(self, host, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((host, port))
            server_socket.listen(5)
            print("Modbus TCP Slave is listening on {}:{}".format(host, port))

            while True:
                client_socket, client_address = server_socket.accept()
                print("New connection from:", client_address)
                thread = Thread(target=self.handle_client, args=(client_socket,))
                thread.start()

    def handle_client(self, client_socket):
        while True:
            irr1 = []
            irr2 = []
            irr3 = []
            Tamb = []
            Tmod = []
            WindS = []
            WindD = []
            Hum = []
            Rain = []
            data = client_socket.recv(1024)
            if not data:
                print('broken')
                break
            seq = data[0:2].hex()
            # print(seq)
            ID = data[6:7].hex()
            func = data[7:8].hex()
            LENS = data[11:12].hex()
            if ID == DevID:
                if func == FUNC:
                    if LENS == datalens:
                        with open(path, newline='') as csvfile:
                            rows = csv.reader(csvfile, delimiter='\t')
                            for row in rows:
                                irr1.append(float(row[10]))
                                irr2.append(float(row[11]))
                                irr3.append(float(row[12]))
                                Tamb.append(float(row[27]))
                                Tmod.append(float(row[20]))
                                WindS.append(float(row[22]))
                                WindD.append(float(row[23]))
                                Rain.append(float(row[21]))
                                Hum.append(float(row[28]))
                            csvlen = len(irr1) - 1
                            IRR1 = struct.pack('>f', irr1[csvlen])
                            IRR2 = struct.pack('>f', irr2[csvlen])
                            IRR3 = struct.pack('>f', irr3[csvlen])
                            TAMB = struct.pack('>f', Tamb[csvlen])
                            TMOD = struct.pack('>f', Tmod[csvlen])
                            WINS = struct.pack('>f', WindS[csvlen])
                            WIND = struct.pack('>f', WindD[csvlen])
                            RAINsen = struct.pack('>f', Rain[csvlen])
                            Humsen = struct.pack('>f', Hum[csvlen])
                        respond = ((bytes.fromhex('%s%s%s%s' % (seq, '00000081', DevID,
                                                                '0378')) + IRR1 + IRR2 + IRR3 + TAMB + TMOD + WINS + WIND + RAINsen + Humsen + IRR1 + IRR2 + IRR3 + TAMB + TMOD + WINS + WIND + RAINsen + Humsen + IRR1 + IRR2 + IRR1 + IRR2 + IRR3 + TAMB + TMOD + WINS + WIND + RAINsen + Humsen + IRR1))
                        # WattClean,VoltageClean,CurrentClean,kWhClean,WattDust,VoltageDust,CurrentDust,kWhDust,Irr,T_amb,T_Dust,T_Clean,Watertanklevel,Windspeed,Winddirection,VoltagePump,CurrentPump,Rainfall,Soiling,Efffect,T_Tank

                        client_socket.sendall(respond)
                        # with open(pathtoday, 'a+', newline='') as csvfile:
                        #     writer = csv.writer(csvfile)
                        #     data = data.hex()
                        #     time1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        #     writer.writerow(
                        #         [time1, data, irr1[csvlen], irr2[csvlen], irr3[csvlen], Tamb[csvlen],
                        #          Tmod[csvlen], WindS[csvlen], WindD[csvlen], Rain[csvlen], Hum[csvlen]])
                        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), 'Senddata OK')
                        del irr1[:]
                        del irr2[:]
                        del irr3[:]
                        del Tamb[:]
                        del Tmod[:]
                        del WindS[:]
                        del WindD[:]
                        del Hum[:]
                        del Rain[:]

        client_socket.close()

# 使用示例
modbus_slave = ModbusTCPSlave.getInstance()
console_observer = ConsolePrintObserver()
modbus_slave.attach(console_observer)
modbus_slave.start("192.168.4.50", 502)