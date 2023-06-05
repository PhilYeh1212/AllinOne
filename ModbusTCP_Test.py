import os
import csv
import time
import struct
import socket

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


while True:
    # if os.path.isfile(pathtoday):
    #     pass
    # else:
    #     with open(pathtoday, 'a+', newline='') as csvfile:
    #         writer = csv.writer(csvfile)
    #         time1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    #         writer.writerow(['Time', 'RevCMD', 'GHI', 'POA', 'Rear', 'Tamb', 'Tmod', 'WindSpeed', 'WindDrection'])

    try:
        Module1_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Module1_TCP.bind(('192.168.4.50', 502))
        Module1_TCP.settimeout(300)
        Module1_TCP.listen(5)
        print('Wait for Command')
        try:
            conn, addr = Module1_TCP.accept()
            with conn:
                conn.settimeout(360)
                print('Connected by', addr)
                print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
                while True:
                    Currentday = time.strftime('%y_%m_%d', time.localtime())
                    # if (today != Currentday):
                    #     today = Currentday
                    #     pathtoday = '%s_%s%s' % ('Weather_station_log', today, '.csv')
                    #     file = str(today + '_buffer for 10.csv')
                    #     path = '%s\%s' % (r"C:\DDS Data", file)
                    #     with open(pathtoday, 'a+', newline='') as csvfile:
                    #         writer = csv.writer(csvfile)
                    #         time1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    #         writer.writerow(
                    #             ['Time', 'RevCMD', 'GHI', 'POA', 'Rear', 'Tamb', 'Tmod', 'WindSpeed', 'WindDrection', 'Rain', 'Hum'])

                    irr1 = []
                    irr2 = []
                    irr3 = []
                    Tamb = []
                    Tmod = []
                    WindS = []
                    WindD = []
                    Hum = []
                    Rain = []
                    data = conn.recv(1024)
                    if not data:
                        print('broken')
                        break
                    seq = data[0:2].hex()
                    #print(seq)
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
#WattClean,VoltageClean,CurrentClean,kWhClean,WattDust,VoltageDust,CurrentDust,kWhDust,Irr,T_amb,T_Dust,T_Clean,Watertanklevel,Windspeed,Winddirection,VoltagePump,CurrentPump,Rainfall,Soiling,Efffect,T_Tank

                                conn.sendall(respond)
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
        except Exception as e:
            print(e)
    except Exception as e:
        print(e)
        print('Wait for Router')
        time.sleep(60)




