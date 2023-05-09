import os
import time
import zipfile

today = time.strftime('%y%m%d', time.localtime())
datafiles = os.listdir(r'C:\HTTPpy\temp')
datafileslen = len(datafiles)
for datafileslen in datafiles:
    try:
        if datafileslen != today:
            with zipfile.ZipFile('%s%s'% (datafileslen, '.zip'), mode='w') as zf:
                # 加入要壓縮的檔案
                zf.write(datafileslen)
        else:
            pass
    except Exception as e:
        print(e)