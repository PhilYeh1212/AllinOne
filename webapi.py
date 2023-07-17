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

@app.route('/SoilingDAS01', methods=['GET'])
def getSoilingDAS01():
    mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306, database="das2_82")
    sql1 = 'SELECT date, Soiling FROM Daily_soiling Order by date desc Limit 1'
    cursor = mydb.cursor()
    cursor.execute(sql1)
    soiling = cursor.fetchall()
    data = {'date': soiling[0][0], 'Soiling': soiling[0][1]}
    return data

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8001, debug=True)