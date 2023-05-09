import time
import requests
import mysql.connector
#aUGMBQKt3BvG82Ymd0jcrnI6Ec9HxRZ6UxGCsglndeB
token = 'aEOyI6xY8bDuzLsCt8bopFL2kDXHHsKg85gzGhnupYE'

def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code

#mydb = mysql.connector.connect(host="localhost",user="root",passwd="Oerlikon;1234",)
#mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306)
data = []
Notupload = []
mydb = mysql.connector.connect(host="localhost", user="root", password="Oerlikon;1234", port=3306, database="FS_Logger_Global")
Today = time.strftime('%Y/%m/%d', time.localtime())
print(Today)
sql1 = "%s'%s'" % ('SELECT Extel_code FROM FS_Logger_Global.Site_list where DAQ_DAte != ', Today)
print(sql1)
cursor1 = mydb.cursor()
cursor1.execute(sql1)
Online = cursor1.fetchall()
print(Online)

for k in Online:
    Extel_code = k
    Notupload.append(Extel_code[0])

num = len(Notupload)

if num <= 0:
    message = "OK"
    lineNotifyMessage(token, message)
if num > 0:
    #message = '%s\n%s:%s%s:%s\n%s:%s' % ('\n缺資料機台', 'Date', date1, 'ID', DAS1, 'Count', Count1)
    message = ((('未正常上傳案場共'+str(num)+'場'), sorted(Notupload)))
    lineNotifyMessage(token, message)
