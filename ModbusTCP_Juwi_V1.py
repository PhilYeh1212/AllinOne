import os
import csv
import time
import struct
import socket

today = time.strftime('%y_%m_%d', time.localtime())

pathtoday = str('ModbusTCP_log_' + today + '.csv')
# print(file)
file = str(today + '.csv')
path = '%s\%s' % (r"C:\DDS Data", file)
# print(path)
DevID = '01'
FUNC = '03'
datalens = '3c'

while True:
    if os.path.isfile(pathtoday):
        pass
    else:
        with open(pathtoday, 'a+', newline='') as csvfile:
            writer = csv.writer(csvfile)
            time1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            writer.writerow(['Time', 'RevCMD', 'WattPV1', 'VolPV1', 'CurPV1', 'kwhPV1', 'WattPV2', 'VolPV2', 'CurPV2',
                             'kwhPV2', 'VolPump', 'CurPump', 'Wind', 'Wins',
                             'Irr', 'Level', 'TClean', 'TDust', 'TEnv', 'TTank', 'Rain', 'Soiling', 'Spare', 'Spare'
                             , 'Spare', 'Spare', 'Spare', 'Spare', 'Spare', 'Spare', 'Spare', 'Spare'])

    try:
        Module1_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Module1_TCP.bind(('172.24.14.161', 502))
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
                    if today != Currentday:
                        today = Currentday
                        pathtoday = '%s_%s%s' % ('ModbusTCP_log_', today, '.csv')
                        file = str(today + '_buffer for 10.csv')
                        path = '%s\%s' % (r"C:\DDS Data", file)
                        with open(pathtoday, 'a+', newline='') as csvfile:
                            writer = csv.writer(csvfile)
                            time1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                            writer.writerow(
                                ['Time', 'RevCMD', 'WattPV1', 'VolPV1', 'CurPV1', 'kwhPV1', 'WattPV2', 'VolPV2',
                                 'CurPV2',
                                 'kwhPV2', 'VolPump', 'CurPump', 'Wind', 'Wins',
                                 'Irr', 'Level', 'TClean', 'TDust', 'TEnv', 'TTank', 'Rain', 'Soiling', 'Spare', 'Spare'
                                    , 'Spare', 'Spare', 'Spare', 'Spare', 'Spare', 'Spare', 'Spare', 'Spare'])

                    WattPV1 = []
                    VolPV1 = []
                    CurPV1 = []
                    kwhPV1 = []
                    WattPV2 = []
                    VolPV2 = []
                    CurPV2 = []
                    kwhPV2 = []
                    VolPump = []
                    CurPump = []
                    Wind = []
                    Wins = []
                    Irr = []
                    Level = []
                    TClean = []
                    TDust = []
                    TEnv = []
                    TTank = []
                    Rain = []
                    Soiling = []
                    data = conn.recv(1024)
                    if not data:
                        print('broken')
                        break
                    seq = data[0:2].hex()
                    ID = data[6:7].hex()
                    func = data[7:8].hex()
                    LENS = data[11:12].hex()
                    if ID == DevID:
                        if func == FUNC:
                            if LENS == datalens:
                                with open(path, newline='') as csvfile:
                                    rows = csv.reader(csvfile, delimiter='\t')
                                    for row in rows:
                                        WattPV1.append(float(row[2]))
                                        VolPV1.append(float(row[3]))
                                        CurPV1.append(float(row[4]))
                                        kwhPV1.append(float(row[5]))
                                        WattPV2.append(float(row[6]))
                                        VolPV2.append(float(row[7]))
                                        CurPV2.append(float(row[8]))
                                        kwhPV2.append(float(row[9]))
                                        VolPump.append(float(row[10]))
                                        CurPump.append(float(row[11]))
                                        Wind.append(float(row[12]))
                                        Wins.append(float(row[13]))
                                        Irr.append(float(row[14]))
                                        Level.append(float(row[15]))
                                        TClean.append(float(row[16]))
                                        TDust.append(float(row[17]))
                                        TEnv.append(float(row[18]))
                                        TTank.append(float(row[19]))
                                        Rain.append(float(row[20]))
                                        Soiling.append(float(row[21]))
                                    csvlen = len(Irr) - 1
                                    WPV1 = struct.pack('>f', WattPV1[csvlen])
                                    VPV1 = struct.pack('>f', VolPV1[csvlen])
                                    CPV1 = struct.pack('>f', CurPV1[csvlen])
                                    kWPV1 = struct.pack('>f', kwhPV1[csvlen])
                                    WPV2 = struct.pack('>f', WattPV2[csvlen])
                                    VPV2 = struct.pack('>f', VolPV2[csvlen])
                                    CPV2 = struct.pack('>f', CurPV2[csvlen])
                                    kWPV2 = struct.pack('>f', kwhPV2[csvlen])
                                    VPump = struct.pack('>f', VolPump[csvlen])
                                    CPump = struct.pack('>f', CurPump[csvlen])
                                    WD = struct.pack('>f', Wind[csvlen])
                                    WS = struct.pack('>f', Wins[csvlen])
                                    IRR = struct.pack('>f', Irr[csvlen])
                                    WLevel = struct.pack('>f', Level[csvlen])
                                    TC = struct.pack('>f', TClean[csvlen])
                                    TD = struct.pack('>f', TDust[csvlen])
                                    TE = struct.pack('>f', TEnv[csvlen])
                                    TT = struct.pack('>f', TTank[csvlen])
                                    RainGage = struct.pack('>f', Rain[csvlen])
                                    EGap = struct.pack('>f', Soiling[csvlen])
                                    Spare = struct.pack('>f', 0)

                                respond = ((bytes.fromhex('%s%s%s%s' % (seq, '00000081', DevID,
                                                                        '0378')) + WPV1 + VPV1 + CPV1 + kWPV1 + WPV2
                                            + VPV2 + CPV2 + kWPV2 + IRR + TE + TD + TC + WLevel + WS + WD + VPump
                                            + CPump + RainGage + EGap + TT + Spare + Spare + Spare + Spare + Spare
                                            + Spare + Spare + Spare + Spare + Spare))

                                conn.sendall(respond)
                                with open(pathtoday, 'a+', newline='') as csvfile:
                                    writer = csv.writer(csvfile)
                                    data = data.hex()
                                    time1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                                    writer.writerow(
                                        [time1, data, WattPV1[csvlen], VolPV1[csvlen], CurPV1[csvlen], kwhPV1[csvlen],
                                         WattPV2[csvlen], VolPV2[csvlen], CurPV2[csvlen], kwhPV2[csvlen],
                                         VolPump[csvlen], TClean[csvlen], TDust[csvlen], TEnv[csvlen],
                                         TTank[csvlen], Rain[csvlen], Soiling[csvlen], Spare, Spare, Spare
                                         , Spare, Spare, Spare, Spare, Spare, Spare, Spare])
                                print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), 'Send-data OK')
                                del WattPV1[:]
                                del VolPV1[:]
                                del CurPV1[:]
                                del kwhPV1[:]
                                del WattPV2[:]
                                del VolPV2[:]
                                del CurPV2[:]
                                del kwhPV2[:]
                                del VolPump[:]
                                del CurPump[:]
                                del Wind[:]
                                del Wins[:]
                                del Irr[:]
                                del Level[:]
                                del TClean[:]
                                del TDust[:]
                                del TEnv[:]
                                del TTank[:]
                                del Rain[:]
                                del Soiling[:]
        except Exception as e:
            print(e)
    except Exception as e:
        print(e)
        print('Wait for Router')
        time.sleep(60)
