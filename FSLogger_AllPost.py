import time
import requests
import mysql.connector
from datetime import datetime
#aUGMBQKt3BvG82Ymd0jcrnI6Ec9HxRZ6UxGCsglndeB
token = '4cwTgoUM0Npnnob1D0aUHCYWxN6huiqVF9poI0G1Efe'
token1 = 'm5BLQpAdN59r03HqH1F0DjhOi9kqFqeL2Viz9n0JYvb'
token2 = '9qRjDI2UAvc2GjNHHUQLaOQKTboxm8mSa5siXPOr7Uh'
token3 = 'SyWs1WJYP64Navfp896JYMkaCItDzO8aBJxkDG6HvCH'
token4 = 'GRN2u7qcUOMphlLnNqydNiILFDYOPOaEUo3XSY88A9a'
token5 = 'WtTLOaHA3CWakWsLSoXJuU5obFNRcjZC3Cu706nWsYJ'
token6 = '6xVzbySPonIyGFgaMIwWcmuY3nNZJVIswFKp57xDCri'
token7 = '1DHgUiZ1P7iOD68qlYVSWD1AwWp2iXZYFFA5KKIA9Tl'
token8 = 'HPAV6BIvbpa9gi8onEFSfUjr72ZJ6CQy7C3jqZBgHNW'
token9 = 'fvBxdNODztqJDyE4K9fh4JVSemgp72geccZDdTmk3NE'
token10 = 'sevvoVXJM23wFDV2VFNkzryRcSxzkIVCpHf5jL72yYv'

data = ''
host = '35.236.181.75'
user = 'root'
password = 'Oerlikon;1234'
database = 'linebot_test'

def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code

Notupload = []
mydb = mysql.connector.connect(host="35.221.247.182", user="root", password="Oerlikon;1234", port=3306, database="FS_Logger_Global")
#mydb = mysql.connector.connect(host="localhost", user="root", password="Oerlikon;1234", port=3306, database="FS_Logger_Global")
Today = time.strftime('%Y/%m/%d', time.localtime())



# # 自檢2
# sql1 = "%s'%s'" % ('SELECT Extel_code FROM FS_Logger_Global.Site_list where DAQ_Date != ', Today)
# cursor1 = mydb.cursor()
# cursor1.execute(sql1)
# Online = cursor1.fetchall()
# for k in Online:
#     Extel_code = k
#     Notupload.append(Extel_code[0])
# num1 = len(Notupload)
# if num1 <= 0:
#     message = "案場正常上傳"
#     lineNotifyMessage(token2, message)
# if num1 > 0:
#     message = ((('未正常上傳案場共'+str(num1)+'場'), sorted(Notupload)))
#     lineNotifyMessage(token1, message)


# 自檢2
connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)


cursor = connection.cursor()

try:

    today = datetime.now().strftime('%Y/%m/%d')
    query = f"SELECT Yesterday FROM everyday_online WHERE Date = '{today}'"
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results[0]:
        data = row
    message = f"昨日未完全上傳資料案場'{data}'\n"
    lineNotifyMessage(token2, message)
except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    cursor.close()
    connection.close()



# 自檢3
StartTime = '00:00:00'
EndTime = '05:00:00'
data2 = []
NightPower = []
NightPower1 = []
NightPowerError =[]
k = 0
sitecode2 = []
with open(r'C:\FS100.txt', 'r') as f:
    for i in range(0,100):
        sitecode2.append(f.readline().replace('\n', ''))
        sql2 = "%s%s.%s %s'%s'%s'%s'%s'%s'" % ('SELECT INVID FROM FSLG_', sitecode2[i], 'T2_inv where INVXX08 > 100', 'and DAQ_DAte =', Today,' and DAQ_Time BETWEEN ', StartTime, ' AND ', EndTime)
        print(sql2)
        sql3 = "SELECT Site_code, Extel_code FROM FS_Logger_Global.Site_list"
        cursor2 = mydb.cursor()
        cursor2.execute(sql2)
        night = cursor2.fetchall()
        if not night:
            pass
        else:
            data2 = sitecode2[i]
            NightPower.append(data2)
    cursor2 = mydb.cursor()
    cursor2.execute(sql3)
    FS1002 = cursor2.fetchall()
    for q in range(len(FS1002)):
        for w in range(len(NightPower)):
            if (FS1002[q][0] == NightPower[w]):
                NightPower1.append(FS1002[q])
    while k < len(NightPower1):
        NightPowerError.append(NightPower1[k][1])
        k = k + 1

    num2 = len(NightPowerError)

    if num2 <= 0:
        message = "無夜間Power"
        lineNotifyMessage(token3, message)
    if num2 > 0:
        message = ((('夜間Inverter有讀值案場'+str(num2)+'場'), sorted(NightPowerError)))
        lineNotifyMessage(token3, message)

#自檢4
StartTime = '10:00:00'
EndTime = '10:03:00'
k = 0
Zero = []
ZeroPower = []
sitecode8 = []

with open(r'C:\FS100.txt', 'r') as f:
    for i in range(0, 100):
        sitecode8.append(f.readline().replace('\n', ''))
        sql13 = "%s%s.%s %s'%s'%s'%s'%s'%s'" % ('SELECT INVID FROM FSLG_', sitecode8[i], 'T2_inv where INVXX08 <= 0', 'and DAQ_DAte =', Today,' and DAQ_Time BETWEEN ', StartTime, ' AND ', EndTime)
        sql14 = "SELECT Site_code, Extel_code FROM FS_Logger_Global.Site_list"
        print(sql13)
        cursor12 = mydb.cursor()
        cursor12.execute(sql13)
        ZeroOnline = cursor12.fetchall()
        cursor13 = mydb.cursor()
        cursor13.execute(sql14)
        FS100 = cursor13.fetchall()
        if not ZeroOnline:
            pass
        else:
            data, Invcode1 = sitecode8[i], ZeroOnline
            Invcode1 = ' '.join(str(i) for i in Invcode1)
            Invcode1 = Invcode1.replace('(', '').replace(',', '').replace(')', '')
            for q in range(len(FS100)):
                if (FS100[q][0]) == (data):
                    ZeroPower.append(FS100[q][1]+'_'+data + '_' + Invcode1 + '\n')
    num = len(ZeroPower)
    print(ZeroPower)
    if num <= 0:
        message = "Inverter發電量為零_全案場正常"
        lineNotifyMessage(token4, message)
    if num > 0:
        message = ((('Inverter發電量為零案場' + str(num) + '場' + '\n'), sorted(ZeroPower)))
        lineNotifyMessage(token4, message)

# 自檢5
StartTime = '09:56:00'
EndTime = '10:00:00'
InverterError = []
k = 0
data4 = []
sitecode4 = []

with open(r'C:\FS100.txt', 'r') as f:
    for i in range(0, 100):
        sitecode4.append(f.readline().replace('\n', ''))
        sql5 = "%s%s.%s %s'%s'%s'%s'%s'%s'" % ('SELECT INVID, INVXX02, INVXX03 FROM FSLG_', sitecode4[i], 'T2_inv where (INVXX02 > 0 or INVXX03 > 0 and INVXX03 < 100) ' , 'and DAQ_DAte =', Today,' and DAQ_Time BETWEEN ', StartTime, ' AND ', EndTime)
        print(sql5)
        sql6 = "SELECT Site_code, Extel_code, inverter FROM FS_Logger_Global.Site_list"
        cursor4 = mydb.cursor()
        cursor4.execute(sql5)
        InverterErrorCode = cursor4.fetchall()
        cursor5 = mydb.cursor()
        cursor5.execute(sql6)
        FS1004 = cursor5.fetchall()
        if not InverterErrorCode:
            pass
        else:
            data4, Invcode2 = sitecode4[i], InverterErrorCode
            Invcode2 = ' '.join(str(i) for i in Invcode2)
            print(Invcode2)
            Invcode2 = Invcode2.replace(' ', '').replace('', '')
            for q in range(len(FS1004)):
                if (FS1004[q][0]) == (data4):
                    InverterError.append(FS1004[q][1]+'_'+data4+'_'+FS1004[q][2]+Invcode2 + '\n')
    num4 = len(InverterError)
    print(InverterError)
    if num4 <= 0:
        message = "Inverter皆無ErrorCode"
        lineNotifyMessage(token5, message)
    if num4 > 0:
        message = ((('Inverter有ErrorCode案場'+str(num4)+'場'+'\n'), sorted(InverterError)))
        lineNotifyMessage(token5, message)


# # # 自檢1
#
#
# connection = mysql.connector.connect(
#     host=host,
#     user=user,
#     password=password,
#     database=database
# )
#
#
# cursor = connection.cursor()
#
# try:
#
#     today = datetime.now().strftime('%Y/%m/%d')
#     query = f"SELECT Number FROM everyday_online WHERE Date = '{today}'"
#     cursor.execute(query)
#     results = cursor.fetchall()
#     for row in results[0]:
#         data = row
#     message = f"案場 '{data}'今日6-8點沒有資料。\n"
#     lineNotifyMessage(token1, message)
# except mysql.connector.Error as err:
#     print(f"Error: {err}")
#
# finally:
#     cursor.close()
#     connection.close()



# Line Notify API 的 URL
url = 'https://notify-api.line.me/api/notify'

# 要傳送的訊息文字
# 準備照片檔案
CGdas = {'imageFile': (r'D:\TPC\static\CG_soiling_chart.jpg', open(r'D:\TPC\static\CG_soiling_chart.jpg', 'rb'), 'image/jpeg')}
#CGdas = {'imageFile': ('C:\_Phil\CG_soiling_chart.jpg', open('photo.jpg', 'rb'), 'image/jpeg')}
# 設定 Header，包含 Authorization 資訊
headers = {
    'Authorization': f'Bearer {token9}'
}
CGmessage = '彰光Soiling'
# 處理請求
response = requests.post(url, headers=headers, files=CGdas, data={'message': CGmessage})

# 檢查回應
if response.status_code == 200:
    print('訊息傳送成功！')
else:
    print(f'訊息傳送失敗，錯誤碼：{response.status_code}，錯誤訊息：{response.text}')

# Line Notify API 的 URL
url = 'https://notify-api.line.me/api/notify'

# 要傳送的訊息文字
# 準備照片檔案
LJdas = {'imageFile': (r'D:\TPC\static\LJ_soiling_chart.jpg', open(r'D:\TPC\static\LJ_soiling_chart.jpg', 'rb'), 'image/jpeg')}
#LJdas = {'imageFile': ('C:\_Phil\LJ_soiling_chart.jpg', open('photo.jpg', 'rb'), 'image/jpeg')}
# 設定 Header，包含 Authorization 資訊
headers = {
    'Authorization': f'Bearer {token10}'
}
LJmessage = '龍井Soiling'
# 處理請求
response = requests.post(url, headers=headers, files=LJdas, data={'message': LJmessage})

# 檢查回應
if response.status_code == 200:
    print('訊息傳送成功！')
else:
    print(f'訊息傳送失敗，錯誤碼：{response.status_code}，錯誤訊息：{response.text}')

# # StartTime = '09:00:00'
# # EndTime = '09:00:00'
# # Count300 = []
# k = 0
# #print(Today)
# data5 = []
# sitecode5 = []
#
# with open(r'C:\FS100.txt', 'r') as f:
#     for i in range(0,100):
#         sitecode5.append(f.readline().replace('\n', ''))
#         sql7 = "%s%s.%s '%s'%s" % ('SELECT count(DAQ_Date) FROM FSLG_', sitecode5[i], 'T1_head where DAQ_Date = (SELECT DATE_FORMAT(subdate(CURDATE(),1),','%Y/%m/%d', '))')
#         print(sql7)
#         sql8 = "SELECT Site_code, Extel_code FROM FS_Logger_Global.Site_list"
#         cursor6 = mydb.cursor()
#         cursor6.execute(sql7)
#         Count285 = cursor6.fetchall()
#         cursor7 = mydb.cursor()
#         cursor7.execute(sql8)
#         FS1005 = cursor7.fetchall()
#         if not Count285:
#             pass
#         elif Count285[0][0] < 285 or Count285[0][0] > 300:
#             data5, count1 = sitecode5[i], Count285[0][0]
#             for q in range(len(FS1005)):
#                 if (FS1005[q][0]) == (data5):
#                     Count300.append(FS1005[q][1]+'_'+data5 + '_' + str(count1) + '\n')
#         else:
#             pass
#     num5 = len(Count300)
#     print(Count300)
#     if num5 <= 0:
#         message = "Count<285 or Count>300_全案場正常"
#         lineNotifyMessage(token5, message)
#     if num5 > 0:
#         message = ((('Count<285 or Count>300案場'+str(num5)+'場'+'\n'), sorted(Count300)))
#         lineNotifyMessage(token5, message)
#
# data6 = []
# StartTime = '10:00:00'
# EndTime = '10:00:00'
# Inverter10000 = []
# k = 0
# #print(Today)
#
# sitecode6 = []
#
# with open(r'C:\FS100.txt', 'r') as f:
#     for i in range(0,100):
#         sitecode6.append(f.readline().replace('\n', ''))
#         sql9 = "%s%s.%s %s'%s'%s" % ('SELECT INVID FROM FSLG_', sitecode6[i], 'T2_inv where INVXX08 > 100000', 'and DAQ_Date = (SELECT DATE_FORMAT(subdate(CURDATE(),1),','%Y/%m/%d', '))')
#         print(sql9)
#         sql10 = "SELECT Site_code, Extel_code FROM FS_Logger_Global.Site_list"
#         cursor8 = mydb.cursor()
#         cursor8.execute(sql9)
#         Inverterover = cursor8.fetchall()
#         cursor9 = mydb.cursor()
#         cursor9.execute(sql10)
#         FS1006 = cursor9.fetchall()
#         if not Inverterover:
#             pass
#         else:
#             data6, Invcode3 = sitecode6[i], Inverterover
#             Invcode3 = ' '.join(str(i) for i in Invcode3)
#             Invcode3 = Invcode3.replace('(', '').replace(',', '').replace(')', '')
#             for q in range(len(FS1006)):
#                 if (FS1006[q][0]) == (data6):
#                     Inverter10000.append(FS1006[q][1]+'_'+data6 + '_' + Invcode3 + '\n')
#     num6 = len(Inverter10000)
#     print(Inverter10000)
#     if num6 <= 0:
#         message = "Inveter發電量未有超過十萬案場"
#         lineNotifyMessage(token6, message)
#     if num6 > 0:
#         message = ((('Inveter發電量超過十萬案場'+str(num6)+'場'+'\n'), sorted(Inverter10000)))
#         lineNotifyMessage(token6, message)
# # 自檢7
# data7 = []
# StartTime = '06:00:00'
# EndTime = '18:00:00'
# Count140 = []
#
# k = 0
# #print(Today)
#
#
# sitecode7 = []
#
# with open(r'C:\FS100.txt', 'r') as f:
#     for i in range(0,100):
#         sitecode7.append(f.readline().replace('\n', ''))
#         sql11 = "%s%s.%s '%s'%s'%s'%s'%s'%s" % ('SELECT count(DAQ_Date) FROM FSLG_', sitecode7[i], 'T2_inv where invid = 1 and DAQ_Date = (SELECT DATE_FORMAT(subdate(CURDATE(), 1),', '%Y/%m/%d', ')) and DAQ_Time >= ', StartTime, ' AND DAQ_Time < ', EndTime, ' GROUP BY daq_date')
#         print(sql11)
#         sql12 = "SELECT Site_code, Extel_code FROM FS_Logger_Global.Site_list"
#         print(sql12)
#         cursor10 = mydb.cursor()
#         cursor10.execute(sql11)
#         Count145 = cursor10.fetchall()
#         cursor11 = mydb.cursor()
#         cursor11.execute(sql12)
#         FS1007 = cursor11.fetchall()
#         if not Count145:
#             pass
#         elif Count145[0][0] < 140:
#             data7, count2 = sitecode7[i], Count145[0][0]
#             for q in range(len(FS1007)):
#                 if (FS1007[q][0]) == (data7):
#                     Count140.append(FS1007[q][1]+'_'+data7 + '_' + str(count2) + '\n')
#         elif Count145[0][0] > 145:
#             data7, count = sitecode7[i], Count145[0][0]
#             for q in range(len(FS1007)):
#                 if (FS1007[q][0]) == (data7):
#                     Count140.append(FS1007[q][1]+'_'+data7 + '_' + str(count2) + '\n')
#         else:
#             pass
#     num7 = len(Count140)
#     print(Count140)
#     if num7 <= 0:
#         message = "145>Count<140_全案場正常"
#         lineNotifyMessage(token7, message)
#     if num7 > 0:
#         message = ((('145>Count<140案場'+str(num7)+'場'+'\n'), sorted(Count140)))
#         lineNotifyMessage(token7, message)
#
# #自檢8
#
#
# sitecode8 = []
# datarepeat = []
# cont = 0
# with open(r'C:\FS100.txt', 'r') as f:
#     try:
#         for i in range(0, 100):
#             sitecode8.append(f.readline().replace('\n', ''))
#             print(sitecode8[i])
#             select_query = '%s%s.%s' % ("SELECT COUNT(*) AS `total_duplicates` FROM(SELECT `UID`, `DAQ_Date`, `DAQ_Time`, `INVID` FROM FSLG_", sitecode8[i],
#                                      'T2_inv GROUP BY `UID`, `DAQ_Date`, `DAQ_Time`, `INVID` HAVING COUNT(*) > 1 ) '
#                                      'AS duplicate_groups;')
#             cursor11 = mydb.cursor()
#             cursor11.execute(select_query)
#             result = cursor11.fetchall()
#             sqlsitecode = "SELECT Site_code, Extel_code FROM FS_Logger_Global.Site_list"
#             cursor12 = mydb.cursor()
#             cursor12.execute(sqlsitecode)
#             sitecoderepeat = cursor12.fetchall()
#             # 處理查詢結果，只顯示一次資料庫名稱
#             if result[0][0] > 0:
#                 for q in range(len(sitecoderepeat)):
#                     if ((sitecode8[i]) == sitecoderepeat[q][0]):
#                         datarepeat.append(sitecoderepeat[q][1] + '_' + sitecode8[i] + '_' + str(result[0][0]) + '\n')
#                         print(datarepeat)
#         num8 = len(datarepeat)
#         print(datarepeat)
#         if num8 <= 0:
#             message = "DataRepeat_全案場正常"
#             lineNotifyMessage(token8, message)
#         if num8 > 0:
#             message = ((('DataRepeat案場'+str(num8)+'場'+'\n'), sorted(datarepeat)))
#             lineNotifyMessage(token8, message)
#     except Exception as e:
#         print(e)








