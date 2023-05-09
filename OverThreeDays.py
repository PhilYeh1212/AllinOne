import time
import requests
import mysql.connector
#OT7izE28dP4V7lgJggVTEiYbFalfsQm8E6H4J5tWCbT
token = 'whW7Rz136t5OvtOViCxTlSRVf2YAbC7CQxDUpTv8ulm'

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
FTP= []
Lostdata = []
Lost = []

mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306,
                               database="vena_dds_global")
#sql = "SELECT * FROM DataCount ORDER BY Date DESC, COUNT DESC"
sql1 = "SELECT DDS_Comany_DatabaseName FROM machines where LinePost = 'T' and Off_grid = 'F' and FTPupload ='F'"
sql2 = "SELECT ID, Date, DAS, COUNT, Insert_date FROM DAS2_dailycount_XX where date_sub(curdate(), interval 3 day)<=Insert_date"
sql3 = "SELECT DDS_Comany_DatabaseName FROM machines where LinePost = 'T' and FTPupload = 'T'"
cursor1 = mydb.cursor()
cursor1.execute(sql1)
Online = cursor1.fetchall()
print(Online)
cursor2 = mydb.cursor()
cursor2.execute(sql2)
DASdata = cursor2.fetchall()
print(DASdata)
cursor3 = mydb.cursor()
cursor3.execute(sql3)
FTPdata = cursor3.fetchall()

for i in range(len(Online)):
    for j in range(len(DASdata)):
        if (set(Online[i]) < set(DASdata[j])) == True:
            data.append(DASdata[j])

for q in range(len(FTPdata)):
    for w in range(len(DASdata)):
        if (set(FTPdata[q]) < set(DASdata[w])) == True:
            FTP.append(DASdata[w])
#intersection = [x for x in Online for y in DASdata if x == y]


for k in data:
    ID, date, DAS, Count, Insertdate = k
    if (int(Count) < 1100):
        Lostdata.append(DAS)
        if Lostdata.count(DAS) >= 4:
            Lost.append(DAS)


#for y in FTP:
#    ID, date, DAS, Count, Insertdate = y
#    if (int(Count) < 700):
#        Lostdata.append(DAS)
num = len(Lost)
if num <= 0:
    message = "OK"
    lineNotifyMessage(token, message)
if num > 0:
    #message = '%s\n%s:%s%s:%s\n%s:%s' % ('\n缺資料機台', 'Date', date1, 'ID', DAS1, 'Count', Count1)
    message = (('共'+str(num)+'台\n'), sorted((Lost)))
    lineNotifyMessage(token, message)
