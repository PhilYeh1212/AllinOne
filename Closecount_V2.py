import time
import requests
import mysql.connector

#PT24pmSfEmZivLn0owUdxj8eIfP5BSf8G2nIJgO4QwS
#MD6jdB4aSkWeyww6MUZaogbQdQpVi9QmFI30vGNQ0Yt
token = 'G3OSherla7611j3a9oop72QXwgxcQGwlVneFdlLytgC'
data = []
CloseErr = []

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

mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306,
                               database="vena_dds_global")
#sql = "SELECT * FROM DataCount ORDER BY Date DESC, COUNT DESC"
#sql = "SELECT Date, DAS, Opencheck,Insert_date FROM DAS2_opencheck_XX where Opencheck > 0 and DAS< 'das2_39' and Insert_date=(SELECT DATE_FORMAT(CURDATE(),'%Y/%m/%d'))"
sql1 = "SELECT DDS_Comany_DatabaseName FROM machines where LinePost = 'T'"
sql2 = "SELECT DAS, Closecheck FROM DAS2_closecheck_XX where Insert_date=(SELECT DATE_FORMAT(CURDATE(),'%Y/%m/%d'))"
cursor1 = mydb.cursor()
cursor1.execute(sql1)
Online = cursor1.fetchall()
#print(Online)
cursor2 = mydb.cursor()
cursor2.execute(sql2)
DASdata = cursor2.fetchall()
#print(DASdata)
for i in range(len(Online)):
    for j in range(len(DASdata)):
        if (set(Online[i]) < set(DASdata[j])) == True:
            data.append(DASdata[j])
print(data)
#intersection = [x for x in Online for y in DASdata if x == y]
for k in data:
    DAS, Closecheck = k
    if (int(Closecheck) > 0):
        CloseErr.append(DAS)
        print(DAS)
num = len(CloseErr)

if num <= 0:
    message = "OK"
    lineNotifyMessage(token, message)
if  num > 0:
    message = (('未正常關蓋機台共' + str(num) + '台\n'), CloseErr)
    lineNotifyMessage(token, message)
