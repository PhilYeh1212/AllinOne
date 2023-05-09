import os
import time
import requests


print('Version-1.2')
today = time.strftime('%y%m%d', time.localtime())
RAWpathtoday = '%s_%s.%s' % ('API_Log', today, 'txt')
ALMpathtoday = '%s_%s.%s' % ('API_Log_Alarm', today, 'txt')
lastTI = 0
URL1 = 'https://pmsdata.formosasolar.com.tw/realtime/extel'
URL2 = 'https://pmsdata.formosasolar.com.tw/realtime/extel/alarm'
RAWline = ''
ALMline = ''
datafiles = os.listdir(r'C:\HTTPUpload')
datafileslen = len(datafiles)
for datafileslen in datafiles:
    try:
        RAWpaths = os.listdir('%s\%s' % (r'C:\HTTPUpload', datafileslen))
        with open('%s\%s\%s' % (r'C:\HTTPUpload', datafileslen, RAWpaths[1]), 'r') as filesRAW:
            RAWdata = filesRAW.readlines()
            RAWline = str(RAWdata)
            #for lenRAW in RAWdata:
            #    RAWline = RAWline + lenRAW
        with open('%s\%s\%s' % (r'C:\HTTPUpload', datafileslen, RAWpaths[0]), 'r') as filesALM:
            ALMdata = filesALM.readlines()
            ALMline = str(ALMdata)
            #for lenALM in ALMdata:
            #    ALMline = ALMline + lenALM
            timenow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            try:
                uploadlist1 = requests.post(URL1, RAWline)
                print(timenow, datafileslen, uploadlist1)
                with open(RAWpathtoday, 'a+') as RAWtxt:
                    RAWtxt.write(timenow, RAWline)
            except Exception as e:
                with open('%s_%s.%s' % (r'C:\HTTPpy\temp\temp_raw', datafileslen, 'txt'), 'w') as RAWwrite:
                    RAWwrite.write(RAWline)
            try:
                uploadlist2 = requests.post(URL2, ALMline)
                print(timenow, datafileslen, uploadlist2)
                with open(ALMpathtoday, 'a+') as ALMtxt:
                    ALMtxt.write(timenow, ALMline)
            except Exception as e:
                with open('%s_%s.%s' % (r'C:\HTTPpy\temp\temp_alm', datafileslen, 'txt'), 'w') as ALMwrite:
                    ALMwrite.write(ALMline)

            RAWline = ''
            ALMline = ''
    except Exception as e:
        print(e)
