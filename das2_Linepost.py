import time
import requests
import mysql.connector
#OT7izE28dP4V7lgJggVTEiYbFalfsQm8E6H4J5tWCbT
token = '4cwTgoUM0Npnnob1D0aUHCYWxN6huiqVF9poI0G1Efe'
token1 = 'DzEbCObbEpn5P7PVdfOwXVzfWB4CWCg22JeCYsgjYUz'
token2 = 'kUFzoEFjBxRkk9pVcEorxc0Bqiuwb1OvcEYy8rJDVG8'
token3 = 'G3OSherla7611j3a9oop72QXwgxcQGwlVneFdlLytgC'
token4 = '6gEE5rpI3O5dr3KzHL0e9MHNJzQcKkqlR9mcLNfVnFn'
token5 = 'whW7Rz136t5OvtOViCxTlSRVf2YAbC7CQxDUpTv8ulm'
token6 = 'aZl13q5eZsBGjzcK4LQNagbu9FkoT0HD1lvWhY3tiRt'

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
mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306,
                               database="vena_dds_global")
#sql = "SELECT * FROM DataCount ORDER BY Date DESC, COUNT DESC"
sql1 = "SELECT DDS_Comany_DatabaseName FROM machines where LinePost = 'T' and Off_grid = 'F' and FTPupload ='F'"
sql2 = "SELECT ID, Date, DAS, COUNT, Insert_date FROM DAS2_dailycount_XX where Insert_date=(SELECT DATE_FORMAT(NOW(),'%Y/%m/%d'))"
sql3 = "SELECT DDS_Comany_DatabaseName FROM machines where LinePost = 'T' and FTPupload = 'T'"
cursor1 = mydb.cursor()
cursor1.execute(sql1)
Online = cursor1.fetchall()
print(Online)
cursor2 = mydb.cursor()
cursor2.execute(sql2)
DASdata1 = cursor2.fetchall()
print(DASdata1)
cursor3 = mydb.cursor()
cursor3.execute(sql3)
FTPdata = cursor3.fetchall()

for i in range(len(Online)):
    for j in range(len(DASdata1)):
        if (set(Online[i]) < set(DASdata1[j])) == True:
            data.append(DASdata1[j])

for q in range(len(FTPdata)):
    for w in range(len(DASdata1)):
        if (set(FTPdata[q]) < set(DASdata1[w])) == True:
            FTP.append(DASdata1[w])
#intersection = [x for x in Online for y in DASdata if x == y]


for k in data:
    ID, date, DAS, Count, Insertdate = k
    if (int(Count) < 1100):
        Lostdata.append(DAS)

for y in FTP:
    ID, date, DAS, Count, Insertdate = y
    if (int(Count) < 700):
        Lostdata.append(DAS)
num1 = len(Lostdata)
if num1 <= 0:
    message = "OK"
    lineNotifyMessage(token1, message)
if num1 > 0:
    #message = '%s\n%s:%s%s:%s\n%s:%s' % ('\n缺資料機台', 'Date', date1, 'ID', DAS1, 'Count', Count1)
    message = (('缺資料機台共'+str(num1)+'台\n'), sorted((Lostdata)))
    lineNotifyMessage(token1, message)



sql4 = "SELECT ID, Date, DAS, COUNT, Insert_date FROM DAS2_dailycount_XX where Insert_date=(SELECT DATE_FORMAT(NOW(),'%Y/%m/%d'))"
cursor4 = mydb.cursor()
cursor4.execute(sql4)
offgrid = cursor4.fetchall()
offgridLostdata = []
offgriddata = offgrid[53:73]
offgriddata1 = offgrid[132:138]

for i in offgriddata:
    ID, date, DAS, Count, Insertdate = i
    if (int(Count) < 360):
        offgridLostdata.append(DAS)
for j in offgriddata1:
    ID, date, DAS, Count, Insertdate = j
    if (int(Count) < 360):
        offgridLostdata.append(DAS)
num2 = len(offgridLostdata)
print(num2)
print(offgridLostdata)
if num2 <= 0:
    message = "OK"
    lineNotifyMessage(token2, message)
if num2 > 0:
    message = ('缺資料機台共'+str(num2)+'台\n'), offgridLostdata
    lineNotifyMessage(token2, message)


CloseErr = []
Closedata = []
sql5 = "SELECT DDS_Comany_DatabaseName FROM machines where LinePost = 'T'"
sql6 = "SELECT DAS, Closecheck FROM DAS2_closecheck_XX where Insert_date=(SELECT DATE_FORMAT(CURDATE(),'%Y/%m/%d'))"
cursor5 = mydb.cursor()
cursor5.execute(sql5)
Close = cursor5.fetchall()
#print(Online)
cursor6 = mydb.cursor()
cursor6.execute(sql6)
DASdata2 = cursor6.fetchall()
#print(DASdata)
for i in range(len(Close)):
    for j in range(len(DASdata2)):
        if (set(Close[i]) < set(DASdata2[j])) == True:
            Closedata.append(DASdata2[j])
print(Closedata)
#intersection = [x for x in Online for y in DASdata if x == y]
for k in Closedata:
    DAS, Closecheck = k
    if (int(Closecheck) > 0):
        CloseErr.append(DAS)
        print(DAS)
num3 = len(CloseErr)

if num3 <= 0:
    message = "OK"
    lineNotifyMessage(token3, message)
if  num3 > 0:
    message = (('未正常關蓋機台共' + str(num3) + '台\n'), CloseErr)
    lineNotifyMessage(token3, message)


OpenErr= []
Opendata = []
sql7 = "SELECT DDS_Comany_DatabaseName FROM machines where LinePost = 'T'"
sql8 = "SELECT DAS, Opencheck FROM DAS2_opencheck_XX where Insert_date=(SELECT DATE_FORMAT(CURDATE(),'%Y/%m/%d'))"
cursor7 = mydb.cursor()
cursor7.execute(sql7)
Open = cursor7.fetchall()
#print(Online)
cursor8 = mydb.cursor()
cursor8.execute(sql8)
DASdata3 = cursor8.fetchall()
#print(DASdata)
for i in range(len(Open)):
    for j in range(len(DASdata3)):
        if (set(Open[i]) < set(DASdata3[j])) == True:
            Opendata.append(DASdata3[j])
#intersection = [x for x in Online for y in DASdata if x == y]
for k in Opendata:
    DAS, Opencheck = k
    if (int(Opencheck) > 0):
        OpenErr.append(DAS)
num4 = len(OpenErr)

if num4 <= 0:
    message = "OK"
    lineNotifyMessage(token4, message)
if  num4 > 0:
    message = (('未正常開蓋機台共' + str(num4) + '台\n'), OpenErr)
    lineNotifyMessage(token4, message)

Threedata1 = []
FTP1 = []
Lostdata1 = []
Lost = []
sql9 = "SELECT DDS_Comany_DatabaseName FROM machines where LinePost = 'T' and Off_grid = 'F' and FTPupload ='F'"
sql10 = "SELECT ID, Date, DAS, COUNT, Insert_date FROM DAS2_dailycount_XX where date_sub(curdate(), interval 3 day)<=Insert_date"
sql11 = "SELECT DDS_Comany_DatabaseName FROM machines where LinePost = 'T' and FTPupload = 'T'"
cursor9 = mydb.cursor()
cursor9.execute(sql9)
Three = cursor9.fetchall()
cursor10 = mydb.cursor()
cursor10.execute(sql10)
DASdata4 = cursor10.fetchall()
cursor11 = mydb.cursor()
cursor11.execute(sql11)
FTPdata1 = cursor11.fetchall()

for i in range(len(Three)):
    for j in range(len(DASdata4)):
        if (set(Three[i]) < set(DASdata4[j])) == True:
            Threedata1.append(DASdata4[j])

for q in range(len(FTPdata1)):
    for w in range(len(DASdata4)):
        if (set(FTPdata1[q]) < set(DASdata4[w])) == True:
            FTP1.append(DASdata4[w])
#intersection = [x for x in Online for y in DASdata if x == y]


for k in Threedata1:
    ID, date, DAS, Count, Insertdate = k
    if (int(Count) < 1100):
        Lostdata.append(DAS)
        if Lostdata.count(DAS) >= 4:
            Lost.append(DAS)
num5 = len(set(Lost))
if num5 <= 0:
    message = "OK"
    lineNotifyMessage(token5, message)
if num5 > 0:
    #message = '%s\n%s:%s%s:%s\n%s:%s' % ('\n缺資料機台', 'Date', date1, 'ID', DAS1, 'Count', Count1)
    message = (('共'+str(num5)+'台\n'), sorted(set(Lost)))
    lineNotifyMessage(token5, message)

DASID = []
soiling = []
datastr = ''
today = time.strftime('%Y/%m')
date = int(time.strftime('%d')) - 1
yesterday = "'%s/%02d'" % (today, date)
i = 0
while i < 150:
    try:
        #datetime = "FROM DAS2_Irr_S where Date='2022/09/01'"
        datetime = ("%s%s" % ("FROM DAS2_Irr_S where Date=", yesterday))
        #print(datetime)
        #sql = "SELECT ID, Date, DAS, COUNT, Insert_date FROM DAS2_dailycount_XX where Insert_date=(SELECT DATE_FORMAT(NOW(),'%Y/%m/%d'))"
        sql12 = "%s %s%s %s" % ("SELECT", "DAS2_", i, datetime)
        DAS = 'DAS2_' + str(i)
        cursor12 = mydb.cursor()
        cursor12.execute(sql12)
        DASdata5 = cursor12.fetchall()
        i = i + 1
        if float(DASdata5[0][0]) < (-0.01):
            DASID.append(DAS)
            soiling.append(DASdata5[0][0])
    except Exception as e:
        i = i + 1
        print(e)
num6 = len(DASID)
print(num6)
data5 = list(zip(DASID, soiling))

if num6 <= 0:
    message = "OK"
    lineNotifyMessage(token6, message)
if num6 >= 1:
    for y in data5:
        datastr = datastr + str(y[0]) + ',' + str(y[1]) + '\n'
    message = (('負Soiling機台共' + str(num6) + '台\n'), datastr)
    lineNotifyMessage(token6, message)