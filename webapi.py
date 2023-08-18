import mysql.connector
import json
from flask import Flask, request, jsonify

#sitecode = []
# with open(r'C:\soiling.txt', 'r') as f:
#     for i in range(0, 1):
#         sitecode.append(f.readline().replace('\n', ''))
#         sql1 = "%s%s.%s" % ('SELECT date, Soiling FROM ', sitecode[0], 'T1_head Order by date desc Limit 1')
#         cursor = mydb.cursor()
#         cursor.execute(sql1)
#         soiling = cursor.fetchall()



app = Flask(__name__)

@app.route('/list', methods=['GET'])
def listdata():
    daslist = json.dumps({'01':'燦宇二期', '02':'燦宇三期', '03':'永宙B2', '04':'永宙B5', '05':'永宙B9',
        '06':'永宙A3-1', '07':'永宙A6', '08':'東台電機', '09':'廣宇25', '10':'廣宇19', '11':'廣宇07',
        '12':'廣宇30', '13':'廣宇38', '14':'永安', '15':'前鋒子', '16':'南池升壓站8號', '17':'北池升壓站10號',
        '18':'南池升壓站3號', '19':'桃園東和鋼鐵工廠', '20':'桃園東和鋼鐵行政', '21':'台中東和鋼鐵工廠',
        '22':'台中東和鋼鐵行政', '23':'高雄東和鋼鐵D3', '24':'高雄東和鋼鐵D1', '25':'苗栗東和鋼鐵工廠',
        '26':'苗栗東和鋼鐵宿舍', '27':'苗栗東和鋼鐵軋鋼廠', '28':'桃園觀音嘉德創'})
    return daslist



@app.route('/Soiling_01', methods=['GET'])
def SoilingDAS01():
    try:
        mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306, database="das2_23")
        sql1 = 'SELECT date, Soiling FROM Daily_soiling Order by date desc Limit 1'
        cursor = mydb.cursor()
        cursor.execute(sql1)
        soiling = cursor.fetchall()
        data = json.dumps({'date': soiling[0][0], 'Soiling': soiling[0][1]*100})
        return data
    except Exception as e:
        print(e)
        return

@app.route('/Soiling_02', methods=['GET'])
def SoilingDAS02():
    mydb2 = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306, database="das2_24")
    sql2 = 'SELECT date, Soiling FROM Daily_soiling Order by date desc Limit 1'
    cursor2 = mydb2.cursor()
    cursor2.execute(sql2)
    soiling2 = cursor2.fetchall()
    data2 = json.dumps({'date': soiling2[0][0], 'Soiling': soiling2[0][1]*100})
    return data2

@app.route('/Soiling_03', methods=['GET'])
def SoilingDAS03():
    mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306, database="das2_25")
    sql1 = 'SELECT date, Soiling FROM Daily_soiling Order by date desc Limit 1'
    cursor = mydb.cursor()
    cursor.execute(sql1)
    soiling = cursor.fetchall()
    data = json.dumps({'date': soiling[0][0], 'Soiling': soiling[0][1]*100})
    return data

@app.route('/Soiling_04', methods=['GET'])
def SoilingDAS04():
    mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306, database="das2_26")
    sql1 = 'SELECT date, Soiling FROM Daily_soiling Order by date desc Limit 1'
    cursor = mydb.cursor()
    cursor.execute(sql1)
    soiling = cursor.fetchall()
    data = json.dumps({'date': soiling[0][0], 'Soiling': soiling[0][1]*100})
    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=False)