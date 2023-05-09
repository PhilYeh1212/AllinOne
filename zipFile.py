import os
import time
import zipfile
import shutil


def zip_dir(path):
    zf = zipfile.ZipFile('{}.zip'.format(path), 'w', zipfile.ZIP_DEFLATED)

    for root, dirs, files in os.walk(path):
        for file_name in files:
            zf.write(os.path.join(root, file_name))


today = time.strftime('%y%m%d', time.localtime())
datafiles = os.listdir(r'D:\FSLG_PMS\HTTPpy\temp')
datafileslen = len(datafiles)
for datafileslen in datafiles:
    try:
        if datafileslen != today and 'Zipfile.py':
            path = datafileslen
            zip_dir(path)
            file_souce = '%s\%s.%s' % (r'D:\FSLG_PMS\HTTPpy\temp', datafileslen, 'zip')
            file_den = '%s\%s.%s' % (r'D:\FSLG_PMS\HTTPpy\logZip', datafileslen, 'zip')
            shutil.move(file_souce, file_den)
            shutil.rmtree(path)
        else:
            pass
    except Exception as e:
        print(e)
