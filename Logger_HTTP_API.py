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
datafiles = os.listdir(r'D:\FSLG_PMS\HTTPBySPV')
datafileslen = len(datafiles)
if not os.path.isdir('%s\%s' % (r'D:\FSLG_PMS\HTTPpy\temp', today)):
    os.mkdir('%s\%s' % (r'D:\FSLG_PMS\HTTPpy\temp', today))

for SPV in datafiles:
    try:
        RAWpath = os.listdir('%s\%s' % (r'D:\FSLG_PMS\HTTPBySPV', SPV))
        for y in RAWpath:
            rawdatapath = os.listdir('%s\%s\%s' % (r'D:\FSLG_PMS\HTTPBySPV', SPV, y))
            with open('%s\%s\%s\%s' % (r'D:\FSLG_PMS\HTTPBySPV', SPV, y, rawdatapath[1]), 'r') as filesRAW:
                RAWdata = filesRAW.readlines()
                lenRAW = str(RAWdata)
                for lenRAW in RAWdata:
                    RAWline = RAWline + lenRAW
            with open('%s\%s\%s\%s' % (r'D:\FSLG_PMS\HTTPBySPV', SPV, y, rawdatapath[0]), 'r') as filesALM:
                ALMdata = filesALM.readlines()
                lenALM = str(ALMdata)
                for lenALM in ALMdata:
                    ALMline = ALMline + lenALM
            timenow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            try:
                uploadlist1 = session.post(URL1, RAWline)
                print(timenow, y, uploadlist1)
                with open('%s\%s\%s_%s_%s.%s' % (r'D:\FSLG_PMS\HTTPpy\temp', today, 'API_Log', today, y, 'txt'), 'a+') as RAWtxt:
                    RAWtxt.write(timenow + '\n')
                    RAWtxt.write(RAWline)
            except Exception as e:
                with open('%s\%s\%s_%s_%s.%s' % (r'D:\FSLG_PMS\HTTPpy\temp', today, 'API_Log', today, y, 'txt'),
                          'a+') as RAWwrite:
                    RAWtxt.write(timenow, RAWline)
            try:
                uploadlist2 = session.post(URL2, ALMline)
                print(timenow, y, uploadlist2)
                with open('%s\%s\%s_%s_%s.%s' % (r'D:\FSLG_PMS\HTTPpy\temp', today, 'API_Log_Alarm', today, y, 'txt'),
                          'a+') as ALMtxt:
                    ALMtxt.write(timenow + '\n')
                    ALMtxt.write(ALMline)
            except Exception as e:
                with open('%s\%s\%s_%s_%s.%s' % (r'D:\FSLG_PMS\HTTPpy\temp', today, 'API_Log_Alarm', today, y, 'txt'),
                          'a+') as ALMwrite:
                    ALMtxt.write(timenow, ALMline)

            RAWline = ''
            ALMline = ''
    except Exception as e:
        print(e)


