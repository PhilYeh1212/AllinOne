import time
import requests
import mysql.connector

token = '6gEE5rpI3O5dr3KzHL0e9MHNJzQcKkqlR9mcLNfVnFn'
DASID = []
soiling = []
datastr = ''
today = time.strftime('%Y/%m')
date = int(time.strftime('%d')) - 1
yesterday = "'%s/%02d'" % (today, date)

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
i = 0
while i < 150:
    try:
        #datetime = "FROM DAS2_Irr_S where Date='2022/09/01'"
        datetime = ("%s%s" % ("FROM DAS2_Irr_S where Date=", yesterday))
        #print(datetime)
        #sql = "SELECT ID, Date, DAS, COUNT, Insert_date FROM DAS2_dailycount_XX where Insert_date=(SELECT DATE_FORMAT(NOW(),'%Y/%m/%d'))"
        sql2 = "%s %s%s %s" % ("SELECT", "DAS2_", i, datetime)
        DAS = 'DAS2_' + str(i)
        cursor2 = mydb.cursor()
        cursor2.execute(sql2)
        DASdata = cursor2.fetchall()
        i = i + 1
        if float(DASdata[0][0]) < (-0.01):
            DASID.append(DAS)
            soiling.append(DASdata[0][0])
    except Exception as e:
        i = i + 1
        print(e)
num = len(DASID)
print(num)
data = list(zip(DASID, soiling))

if num <= 0:
    message = "OK"
    lineNotifyMessage(token, message)
if num >= 1:
    for y in data:
        datastr = datastr + str(y[0]) + ',' + str(y[1]) + '\n'
    message = (('負Soiling機台共' + str(num) + '台\n'), datastr)
    lineNotifyMessage(token, message)
