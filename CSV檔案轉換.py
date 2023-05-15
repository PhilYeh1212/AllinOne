import os
import csv
import time
import struct
import socket

datafiles = os.listdir(r'C:\_Phil\02_Project\_ChenyaPVQA\data')
path = r'C:\_Phil\02_Project\_ChenyaPVQA\data'
newpath = r'C:\_Phil\02_Project\_ChenyaPVQA\forChenya\5月.csv'
with open(newpath, 'a+', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(
        ['Date', 'Time', 'GHI', 'POA', 'Tamb', 'Tmod', 'WindSpeed', 'WindDrection', 'Rain', 'Hum'])

for data in datafiles:
    print(data)
    with open ('%s\%s' % (path, data), newline='') as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')
        for row in rows:
            with open(newpath, 'a+', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(
                    [row[0], row[1], row[2], row[3], row[10], row[13], row[6], row[5], row[15], row[11]])

