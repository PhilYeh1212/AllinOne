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
#     query = f"SELECT Yesterday FROM everyday_online WHERE Date = '{today}'"
#     cursor.execute(query)
#     results = cursor.fetchall()
#     for row in results[0]:
#         data = row
#     message = f"昨日未完全上傳資料案場'{data}'\n"
#     lineNotifyMessage(token2, message)
# except mysql.connector.Error as err:
#     print(f"Error: {err}")
#
# finally:
#     cursor.close()
#     connection.close()
#
#
#
# # 自檢3
# StartTime = '00:00:00'
# EndTime = '05:00:00'
# data2 = []
# NightPower = []
# NightPower1 = []
# NightPowerError =[]
# k = 0
# sitecode2 = []
# with open(r'C:\FS100.txt', 'r') as f:
#     for i in range(0,100):
#         sitecode2.append(f.readline().replace('\n', ''))
#         sql2 = "%s%s.%s %s'%s'%s'%s'%s'%s'" % ('SELECT INVID FROM FSLG_', sitecode2[i], 'T2_inv where INVXX08 > 100', 'and DAQ_DAte =', Today,' and DAQ_Time BETWEEN ', StartTime, ' AND ', EndTime)
#         print(sql2)
#         sql3 = "SELECT Site_code, Extel_code FROM FS_Logger_Global.Site_list"
#         cursor2 = mydb.cursor()
#         cursor2.execute(sql2)
#         night = cursor2.fetchall()
#         if not night:
#             pass
#         else:
#             data2 = sitecode2[i]
#             NightPower.append(data2)
#     cursor2 = mydb.cursor()
#     cursor2.execute(sql3)
#     FS1002 = cursor2.fetchall()
#     for q in range(len(FS1002)):
#         for w in range(len(NightPower)):
#             if (FS1002[q][0] == NightPower[w]):
#                 NightPower1.append(FS1002[q])
#     while k < len(NightPower1):
#         NightPowerError.append(NightPower1[k][1])
#         k = k + 1
#
#     num2 = len(NightPowerError)
#
#     if num2 <= 0:
#         message = "無夜間Power"
#         lineNotifyMessage(token3, message)
#     if num2 > 0:
#         message = ((('夜間Inverter有讀值案場'+str(num2)+'場'), sorted(NightPowerError)))
#         lineNotifyMessage(token3, message)
#
# #自檢4
# StartTime = '10:00:00'
# EndTime = '10:03:00'
# k = 0
# Zero = []
# ZeroPower = []
# sitecode8 = []
#
# with open(r'C:\FS100.txt', 'r') as f:
#     for i in range(0, 100):
#         sitecode8.append(f.readline().replace('\n', ''))
#         sql13 = "%s%s.%s %s'%s'%s'%s'%s'%s'" % ('SELECT INVID FROM FSLG_', sitecode8[i], 'T2_inv where INVXX08 <= 0', 'and DAQ_DAte =', Today,' and DAQ_Time BETWEEN ', StartTime, ' AND ', EndTime)
#         sql14 = "SELECT Site_code, Extel_code FROM FS_Logger_Global.Site_list"
#         print(sql13)
#         cursor12 = mydb.cursor()
#         cursor12.execute(sql13)
#         ZeroOnline = cursor12.fetchall()
#         cursor13 = mydb.cursor()
#         cursor13.execute(sql14)
#         FS100 = cursor13.fetchall()
#         if not ZeroOnline:
#             pass
#         else:
#             data, Invcode1 = sitecode8[i], ZeroOnline
#             Invcode1 = ' '.join(str(i) for i in Invcode1)
#             Invcode1 = Invcode1.replace('(', '').replace(',', '').replace(')', '')
#             for q in range(len(FS100)):
#                 if (FS100[q][0]) == (data):
#                     ZeroPower.append(FS100[q][1]+'_'+data + '_' + Invcode1 + '\n')
#     num = len(ZeroPower)
#     print(ZeroPower)
#     if num <= 0:
#         message = "Inverter發電量為零_全案場正常"
#         lineNotifyMessage(token4, message)
#     if num > 0:
#         message = ((('Inverter發電量為零案場' + str(num) + '場' + '\n'), sorted(ZeroPower)))
#         lineNotifyMessage(token4, message)

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

        sql5 = sql5.replace(
            "T2_inv where (INVXX02 > 0 or INVXX03 > 0 and INVXX03 < 100)",
            "T2_inv WHERE INVXX02 IN (SELECT index_number FROM FS_Logger_Global.Alarm_index WHERE Text = 'INVXX02') OR INVXX03 IN (SELECT index_number FROM FS_Logger_Global.Alarm_index WHERE Text = 'INVXX03')"
        )
        #sql5 = "%s%s.%s %s'%s'%s'%s'%s'%s'" % ('SELECT INVID, INVXX02, INVXX03 FROM FSLG_', sitecode4[i], 'T2_inv where (INVXX02 > 0 or INVXX03 > 0 and INVXX03 < 100) ' , 'and DAQ_DAte =', Today,' and DAQ_Time BETWEEN ', StartTime, ' AND ', EndTime)
        print(sql5)
        #sql6 = "SELECT Site_code, Extel_code, inverter FROM FS_Logger_Global.Site_list"
        cursor4 = mydb.cursor()
        cursor4.execute(sql5)
    #     InverterErrorCode = cursor4.fetchall()
    #     cursor5 = mydb.cursor()
    #     cursor5.execute(sql6)
    #     FS1004 = cursor5.fetchall()
    #     if not InverterErrorCode:
    #         pass
    #     else:
    #         data4, Invcode2 = sitecode4[i], InverterErrorCode
    #         Invcode2 = ' '.join(str(i) for i in Invcode2)
    #         print(Invcode2)
    #         Invcode2 = Invcode2.replace(' ', '').replace('', '')
    #         for q in range(len(FS1004)):
    #             if (FS1004[q][0]) == (data4):
    #                 InverterError.append(FS1004[q][1]+'_'+data4+'_'+FS1004[q][2]+Invcode2 + '\n')
    # num4 = len(InverterError)
    # print(InverterError)
    # if num4 <= 0:
    #     message = "Inverter皆無ErrorCode"
    #     lineNotifyMessage(token5, message)
    # if num4 > 0:
    #     message = ((('Inverter有ErrorCode案場'+str(num4)+'場'+'\n'), sorted(InverterError)))
    #     lineNotifyMessage(token5, message)


# Line Notify API 的 URL
# url = 'https://notify-api.line.me/api/notify'
#
# # 要傳送的訊息文字
# # 準備照片檔案
# CGdas = {'imageFile': (r'D:\TPC\static\CG_soiling_chart.jpg', open(r'D:\TPC\static\CG_soiling_chart.jpg', 'rb'), 'image/jpeg')}
# #CGdas = {'imageFile': ('C:\_Phil\CG_soiling_chart.jpg', open('photo.jpg', 'rb'), 'image/jpeg')}
# # 設定 Header，包含 Authorization 資訊
# headers = {
#     'Authorization': f'Bearer {token9}'
# }
# CGmessage = '彰光Soiling'
# # 處理請求
# response = requests.post(url, headers=headers, files=CGdas, data={'message': CGmessage})
#
# # 檢查回應
# if response.status_code == 200:
#     print('訊息傳送成功！')
# else:
#     print(f'訊息傳送失敗，錯誤碼：{response.status_code}，錯誤訊息：{response.text}')
#
# # Line Notify API 的 URL
# url = 'https://notify-api.line.me/api/notify'
#
# # 要傳送的訊息文字
# # 準備照片檔案
# LJdas = {'imageFile': (r'D:\TPC\static\LJ_soiling_chart.jpg', open(r'D:\TPC\static\LJ_soiling_chart.jpg', 'rb'), 'image/jpeg')}
# #LJdas = {'imageFile': ('C:\_Phil\LJ_soiling_chart.jpg', open('photo.jpg', 'rb'), 'image/jpeg')}
# # 設定 Header，包含 Authorization 資訊
# headers = {
#     'Authorization': f'Bearer {token10}'
# }
# LJmessage = '龍井Soiling'
# # 處理請求
# response = requests.post(url, headers=headers, files=LJdas, data={'message': LJmessage})
#
# # 檢查回應
# if response.status_code == 200:
#     print('訊息傳送成功！')
# else:
#     print(f'訊息傳送失敗，錯誤碼：{response.status_code}，錯誤訊息：{response.text}')








