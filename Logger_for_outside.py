import os
import time
import requests

print('Version-1.2')
session = requests.session()
today = time.strftime('%y%m%d', time.localtime())
lastTI = 0
URL1 = 'https://pmsdata.formosasolar.com.tw/realtime/extel'
URL2 = 'https://pmsdata.formosasolar.com.tw/realtime/extel/alarm'
RAWline = ''
ALMline = ''
datafiles = os.listdir(r'C:\FTP_Upload')
datafileslen = len(datafiles)
if not os.path.isdir('%s\%s' % (r'C:\LoggerUpload\temp', today)):
    os.mkdir('%s\%s' % (r'C:\LoggerUpload\temp', today))
while True:
    inTi = time.time()
    if inTi - lastTI >= 300:
        try:
            for loggerdata in datafiles:
                timenow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                datapath = os.listdir(r'C:\FTP_Upload')
                with open('%s\%s' % (r'C:\FTP_Upload', datapath[1]), 'r') as filesRAW:
                    RAWdata = filesRAW.readlines()
                    lenRAW = str(RAWdata)
                    for lenRAW in RAWdata:
                        RAWline = RAWline + lenRAW
                with open('%s\%s' % (r'C:\FTP_Upload', datapath[0]), 'r') as filesALM:
                    ALMdata = filesALM.readlines()
                    lenALM = str(ALMdata)
                    for lenALM in ALMdata:
                        ALMline = ALMline + lenALM

            try:
                uploadlist1 = session.post(URL1, RAWline)
                print(timenow, uploadlist1)
                with open('%s\%s\%s_%s.%s' % (r'C:\LoggerUpload\temp', today, 'API_Log', today, 'txt'),
                          'a+') as RAWtxt:
                    RAWtxt.write(timenow + '\n')
                    RAWtxt.write(RAWline)
            except Exception as e:
                with open('%s\%s\%s_%s.%s' % (r'C:\LoggerUpload\temp', today, 'API_Log', today, 'txt'),
                          'a+') as RAWwrite:
                    RAWtxt.write(timenow, RAWline)
            try:
                uploadlist2 = session.post(URL2, ALMline)
                print(timenow, uploadlist2)
                with open(
                        '%s\%s\%s_%s.%s' % (r'C:\LoggerUpload\temp', today, 'API_Log_Alarm', today, 'txt'),
                        'a+') as ALMtxt:
                    ALMtxt.write(timenow + '\n')
                    ALMtxt.write(ALMline)
            except Exception as e:
                with open(
                        '%s\%s\%s_%s.%s' % (r'C:\LoggerUpload\temp', today, 'API_Log_Alarm', today, 'txt'),
                        'a+') as ALMwrite:
                    ALMtxt.write(timenow, ALMline)
            RAWline = ''
            ALMline = ''
            lastTI = time.time()
        except Exception as e:
            print(e)


