import time
import requests
import mysql.connector
#oJSrrZRJhrDzKyvPHi6q0XLgF46kMUGUYs2qnzt8zmn
token = 'aZl13q5eZsBGjzcK4LQNagbu9FkoT0HD1lvWhY3tiRt'


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
sql = "SELECT ID, Date, DAS, COUNT, Insert_date FROM DAS2_dailycount_XX where Insert_date=(SELECT DATE_FORMAT(NOW(),'%Y/%m/%d'))"
cursor = mydb.cursor()
cursor.execute(sql)
myresult = cursor.fetchall()
num = len(myresult)
Lostdata = []
data = myresult[53:73]
data1 = myresult[132:138]

for i in data:
    ID, date, DAS, Count, Insertdate = i
    if (int(Count) < 360):
        Lostdata.append(DAS)
for j in data1:
    ID, date, DAS, Count, Insertdate = j
    if (int(Count) < 360):
        Lostdata.append(DAS)
num = len(Lostdata)
print(num)
print(Lostdata)
if num <= 0:
    message = "OK"
    lineNotifyMessage(token, message)
if num > 0:
    message = ('缺資料機台共'+str(num)+'台\n'), Lostdata
    lineNotifyMessage(token, message)
