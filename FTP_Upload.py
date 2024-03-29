import os
import time
import shutil
import paramiko

year = time.strftime('%Y')
mon = time.strftime('%m')
date = time.strftime('%d')
host = "35.189.175.5"
port = 22
transport = paramiko.Transport((host, port))
f = open(r'C:/pic_FTP_key.txt')
E2path = f.readline()

password = "extel2019"
username = "playplus"

transport.connect(username = username, password = password)
sftp = paramiko.SFTPClient.from_transport(transport)


files = os.listdir(r'C:\pic')
for x in files:
    path = '%s/%s/%s/%s' % ('/home/playplus/www/estpower/public/uploads/DDS_Pic', E2path, 'Upload_buffer', x)
    print(path)
    sourcepath = '%s%s' % ('C:/pic/', x)
    destinationpath = '%s%s' % ('C:/picFTP/', x)
    sftp.put(sourcepath, path)
    shutil.move(sourcepath, destinationpath)

sftp.close()
transport.close()