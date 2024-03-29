import mysql.connector
from flask import Flask, request, jsonify, render_template, json, Response, abort

# sitecode = []
# with open(r'C:\soiling.txt', 'r') as f:
#     for i in range(0, 1):
#         sitecode.append(f.readline().replace('\n', ''))
#         sql1 = "%s%s.%s" % ('SELECT date, Soiling FROM ', sitecode[0], 'T1_head Order by date desc Limit 1')
#         cursor = mydb.cursor()
#         cursor.execute(sql1)
#         soiling = cursor.fetchall()

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
API_KEY = 'sa0u5U4rTTprOVtReJQKXlsAYy7Oihr3'


@app.route('/list', methods=['POST'])
def listdata():
    api_key = request.headers.POST('API-Key')
    if api_key != API_KEY:
        abort(401, 'Unauthorized: Invalid API key')

    json_dict = {'01': '燦宇二期', '02': '燦宇三期', '03': '永宙B2', '04': '永宙B5', '05': '永宙B9',
                 '06': '永宙A3-1', '07': '永宙A6', '08': '東台電機', '09': '廣宇25', '10': '廣宇19', '11': '廣宇07',
                 '12': '廣宇30', '13': '廣宇38', '14': '永安', '15': '前鋒子', '16': '南池升壓站8號', '17': '北池升壓站10號',
                 '18': '南池升壓站3號', '19': '桃園東和鋼鐵工廠', '20': '桃園東和鋼鐵行政', '21': '台中東和鋼鐵工廠',
                 '22': '台中東和鋼鐵行政', '23': '高雄東和鋼鐵D3', '24': '高雄東和鋼鐵D1', '25': '苗栗東和鋼鐵工廠',
                 '26': '苗栗東和鋼鐵宿舍', '27': '苗栗東和鋼鐵軋鋼廠', '28': '桃園觀音嘉德創'}
    response = Response(json.dumps(json_dict, ensure_ascii=False), content_type='application/json;charset=utf-8')
    return response


@app.route('/Soiling_01', methods=['POST'])
def SoilingDAS01():
    api_key = request.headers.POST('API-Key')
    if api_key != API_KEY:
        abort(401, 'Unauthorized: Invalid API key')
    try:
        mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306,
                                       database="das2_23")
        sql1 = 'SELECT date, Soiling FROM Daily_soiling Order by date desc Limit 1'
        cursor = mydb.cursor()
        cursor.execute(sql1)
        soiling = cursor.fetchall()
        data = json.dumps({'date': soiling[0][0], 'Soiling': soiling[0][1] * 100})
        return data
    except Exception as e:
        print(e)
        return 'no data'


@app.route('/Soiling_02', methods=['POST'])
def SoilingDAS02():
    api_key = request.headers.POST('API-Key')
    if api_key != API_KEY:
        abort(401, 'Unauthorized: Invalid API key')
    try:
        mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306,
                                       database="das2_24")
        sql1 = 'SELECT date, Soiling FROM Daily_soiling Order by date desc Limit 1'
        cursor = mydb.cursor()
        cursor.execute(sql1)
        soiling = cursor.fetchall()
        data = json.dumps({'date': soiling[0][0], 'Soiling': soiling[0][1] * 100})
        return data
    except Exception as e:
        print(e)
        return 'no data'


@app.route('/Soiling_03', methods=['POST'])
def SoilingDAS03():
    api_key = request.headers.POST('API-Key')
    if api_key != API_KEY:
        abort(401, 'Unauthorized: Invalid API key')
    try:
        mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306,
                                       database="das2_25")
        sql1 = 'SELECT date, Soiling FROM Daily_soiling Order by date desc Limit 1'
        cursor = mydb.cursor()
        cursor.execute(sql1)
        soiling = cursor.fetchall()
        data = json.dumps({'date': soiling[0][0], 'Soiling': soiling[0][1] * 100})
        return data
    except Exception as e:
        print(e)
        return 'no data'


@app.route('/Soiling_04', methods=['POST'])
def SoilingDAS04():
    api_key = request.headers.POST('API-Key')
    if api_key != API_KEY:
        abort(401, 'Unauthorized: Invalid API key')
    try:
        mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306,
                                       database="das2_26")
        sql1 = 'SELECT date, Soiling FROM Daily_soiling Order by date desc Limit 1'
        cursor = mydb.cursor()
        cursor.execute(sql1)
        soiling = cursor.fetchall()
        data = json.dumps({'date': soiling[0][0], 'Soiling': soiling[0][1] * 100})
        return data
    except Exception as e:
        print(e)
        return 'no data'


@app.route('/Soiling_05', methods=['POST'])
def SoilingDAS05():
    api_key = request.headers.POST('API-Key')
    if api_key != API_KEY:
        abort(401, 'Unauthorized: Invalid API key')
    try:
        mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306,
                                       database="das2_27")
        sql1 = 'SELECT date, Soiling FROM Daily_soiling Order by date desc Limit 1'
        cursor = mydb.cursor()
        cursor.execute(sql1)
        soiling = cursor.fetchall()
        data = json.dumps({'date': soiling[0][0], 'Soiling': soiling[0][1] * 100})
        return data
    except Exception as e:
        print(e)
        return 'no data'


@app.route('/Soiling_06', methods=['POST'])
def SoilingDAS06():
    api_key = request.headers.POST('API-Key')
    if api_key != API_KEY:
        abort(401, 'Unauthorized: Invalid API key')
    try:
        mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306,
                                       database="das2_28")
        sql1 = 'SELECT date, Soiling FROM Daily_soiling Order by date desc Limit 1'
        cursor = mydb.cursor()
        cursor.execute(sql1)
        soiling = cursor.fetchall()
        data = json.dumps({'date': soiling[0][0], 'Soiling': soiling[0][1] * 100})
        return data
    except Exception as e:
        print(e)
        return 'no data'


@app.route('/Soiling_07', methods=['POST'])
def SoilingDAS07():
    api_key = request.headers.POST('API-Key')
    if api_key != API_KEY:
        abort(401, 'Unauthorized: Invalid API key')
    try:
        mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306,
                                       database="das2_29")
        sql1 = 'SELECT date, Soiling FROM Daily_soiling Order by date desc Limit 1'
        cursor = mydb.cursor()
        cursor.execute(sql1)
        soiling = cursor.fetchall()
        data = json.dumps({'date': soiling[0][0], 'Soiling': soiling[0][1] * 100})
        return data
    except Exception as e:
        print(e)
        return 'no data'


@app.route('/Soiling_08', methods=['POST'])
def SoilingDAS08():
    api_key = request.headers.POST('API-Key')
    if api_key != API_KEY:
        abort(401, 'Unauthorized: Invalid API key')
    try:
        mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306,
                                       database="das2_39")
        sql1 = 'SELECT date, Soiling FROM Daily_soiling Order by date desc Limit 1'
        cursor = mydb.cursor()
        cursor.execute(sql1)
        soiling = cursor.fetchall()
        data = json.dumps({'date': soiling[0][0], 'Soiling': soiling[0][1] * 100})
        return data
    except Exception as e:
        print(e)
        return 'no data'


@app.route('/Soiling_09', methods=['POST'])
def SoilingDAS09():
    api_key = request.headers.POST('API-Key')
    if api_key != API_KEY:
        abort(401, 'Unauthorized: Invalid API key')
    try:
        mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306,
                                       database="das2_40")
        sql1 = 'SELECT date, Soiling FROM Daily_soiling Order by date desc Limit 1'
        cursor = mydb.cursor()
        cursor.execute(sql1)
        soiling = cursor.fetchall()
        data = json.dumps({'date': soiling[0][0], 'Soiling': soiling[0][1] * 100})
        return data
    except Exception as e:
        print(e)
        return 'no data'


@app.route('/Soiling_10', methods=['POST'])
def SoilingDAS10():
    api_key = request.headers.POST('API-Key')
    if api_key != API_KEY:
        abort(401, 'Unauthorized: Invalid API key')
    try:
        mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306,
                                       database="das2_41")
        sql1 = 'SELECT date, Soiling FROM Daily_soiling Order by date desc Limit 1'
        cursor = mydb.cursor()
        cursor.execute(sql1)
        soiling = cursor.fetchall()
        data = json.dumps({'date': soiling[0][0], 'Soiling': soiling[0][1] * 100})
        return data
    except Exception as e:
        print(e)
        return 'no data'


@app.route('/Soiling_11', methods=['POST'])
def SoilingDAS11():
    api_key = request.headers.POST('API-Key')
    if api_key != API_KEY:
        abort(401, 'Unauthorized: Invalid API key')
    try:
        mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306,
                                       database="das2_42")
        sql1 = 'SELECT date, Soiling FROM Daily_soiling Order by date desc Limit 1'
        cursor = mydb.cursor()
        cursor.execute(sql1)
        soiling = cursor.fetchall()
        data = json.dumps({'date': soiling[0][0], 'Soiling': soiling[0][1] * 100})
        return data
    except Exception as e:
        print(e)
        return 'no data'


@app.route('/Soiling_12', methods=['POST'])
def SoilingDAS12():
    api_key = request.headers.POST('API-Key')
    if api_key != API_KEY:
        abort(401, 'Unauthorized: Invalid API key')
    try:
        mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306,
                                       database="das2_43")
        sql1 = 'SELECT date, Soiling FROM Daily_soiling Order by date desc Limit 1'
        cursor = mydb.cursor()
        cursor.execute(sql1)
        soiling = cursor.fetchall()
        data = json.dumps({'date': soiling[0][0], 'Soiling': soiling[0][1] * 100})
        return data
    except Exception as e:
        print(e)
        return 'no data'


@app.route('/Soiling_13', methods=['POST'])
def SoilingDAS13():
    api_key = request.headers.POST('API-Key')
    if api_key != API_KEY:
        abort(401, 'Unauthorized: Invalid API key')
    try:
        mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306,
                                       database="das2_44")
        sql1 = 'SELECT date, Soiling FROM Daily_soiling Order by date desc Limit 1'
        cursor = mydb.cursor()
        cursor.execute(sql1)
        soiling = cursor.fetchall()
        data = json.dumps({'date': soiling[0][0], 'Soiling': soiling[0][1] * 100})
        return data
    except Exception as e:
        print(e)
        return 'no data'


@app.route('/Soiling_14', methods=['POST'])
def SoilingDAS14():
    api_key = request.headers.POST('API-Key')
    if api_key != API_KEY:
        abort(401, 'Unauthorized: Invalid API key')
    try:
        mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306,
                                       database="das2_45")
        sql1 = 'SELECT date, Soiling FROM Daily_soiling Order by date desc Limit 1'
        cursor = mydb.cursor()
        cursor.execute(sql1)
        soiling = cursor.fetchall()
        data = json.dumps({'date': soiling[0][0], 'Soiling': soiling[0][1] * 100})
        return data
    except Exception as e:
        print(e)
        return 'no data'


@app.route('/Soiling_15', methods=['POST'])
def SoilingDAS15():
    api_key = request.headers.POST('API-Key')
    if api_key != API_KEY:
        abort(401, 'Unauthorized: Invalid API key')
    try:
        mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306,
                                       database="das2_46")
        sql1 = 'SELECT date, Soiling FROM Daily_soiling Order by date desc Limit 1'
        cursor = mydb.cursor()
        cursor.execute(sql1)
        soiling = cursor.fetchall()
        data = json.dumps({'date': soiling[0][0], 'Soiling': soiling[0][1] * 100})
        return data
    except Exception as e:
        print(e)
        return 'no data'


@app.route('/Soiling_16', methods=['POST'])
def SoilingDAS16():
    api_key = request.headers.POST('API-Key')
    if api_key != API_KEY:
        abort(401, 'Unauthorized: Invalid API key')
    try:
        mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306,
                                       database="das2_49")
        sql1 = 'SELECT date, Soiling FROM Daily_soiling Order by date desc Limit 1'
        cursor = mydb.cursor()
        cursor.execute(sql1)
        soiling = cursor.fetchall()
        data = json.dumps({'date': soiling[0][0], 'Soiling': soiling[0][1] * 100})
        return data
    except Exception as e:
        print(e)
        return 'no data'


@app.route('/Soiling_17', methods=['POST'])
def SoilingDAS17():
    api_key = request.headers.POST('API-Key')
    if api_key != API_KEY:
        abort(401, 'Unauthorized: Invalid API key')
    try:
        mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306,
                                       database="das2_50")
        sql1 = 'SELECT date, Soiling FROM Daily_soiling Order by date desc Limit 1'
        cursor = mydb.cursor()
        cursor.execute(sql1)
        soiling = cursor.fetchall()
        data = json.dumps({'date': soiling[0][0], 'Soiling': soiling[0][1] * 100})
        return data
    except Exception as e:
        print(e)
        return 'no data'


@app.route('/Soiling_18', methods=['POST'])
def SoilingDAS18():
    api_key = request.headers.POST('API-Key')
    if api_key != API_KEY:
        abort(401, 'Unauthorized: Invalid API key')
    try:
        mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306,
                                       database="das2_122")
        sql1 = 'SELECT date, Soiling FROM Daily_soiling Order by date desc Limit 1'
        cursor = mydb.cursor()
        cursor.execute(sql1)
        soiling = cursor.fetchall()
        data = json.dumps({'date': soiling[0][0], 'Soiling': soiling[0][1] * 100})
        return data
    except Exception as e:
        print(e)
        return 'no data'


@app.route('/Soiling_19', methods=['POST'])
def SoilingDAS19():
    api_key = request.headers.POST('API-Key')
    if api_key != API_KEY:
        abort(401, 'Unauthorized: Invalid API key')
    try:
        mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306,
                                       database="das2_123")
        sql1 = 'SELECT date, Soiling FROM Daily_soiling Order by date desc Limit 1'
        cursor = mydb.cursor()
        cursor.execute(sql1)
        soiling = cursor.fetchall()
        data = json.dumps({'date': soiling[0][0], 'Soiling': soiling[0][1] * 100})
        return data
    except Exception as e:
        print(e)
        return 'no data'


@app.route('/Soiling_20', methods=['POST'])
def SoilingDAS20():
    api_key = request.headers.POST('API-Key')
    if api_key != API_KEY:
        abort(401, 'Unauthorized: Invalid API key')
    try:
        mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306,
                                       database="das2_124")
        sql1 = 'SELECT date, Soiling FROM Daily_soiling Order by date desc Limit 1'
        cursor = mydb.cursor()
        cursor.execute(sql1)
        soiling = cursor.fetchall()
        data = json.dumps({'date': soiling[0][0], 'Soiling': soiling[0][1] * 100})
        return data
    except Exception as e:
        print(e)
        return 'no data'


@app.route('/Soiling_21', methods=['POST'])
def SoilingDAS21():
    api_key = request.headers.POST('API-Key')
    if api_key != API_KEY:
        abort(401, 'Unauthorized: Invalid API key')
    try:
        mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306,
                                       database="das2_125")
        sql1 = 'SELECT date, Soiling FROM Daily_soiling Order by date desc Limit 1'
        cursor = mydb.cursor()
        cursor.execute(sql1)
        soiling = cursor.fetchall()
        data = json.dumps({'date': soiling[0][0], 'Soiling': soiling[0][1] * 100})
        return data
    except Exception as e:
        print(e)
        return 'no data'


@app.route('/Soiling_22', methods=['POST'])
def SoilingDAS22():
    api_key = request.headers.POST('API-Key')
    if api_key != API_KEY:
        abort(401, 'Unauthorized: Invalid API key')
    try:
        mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306,
                                       database="das2_126")
        sql1 = 'SELECT date, Soiling FROM Daily_soiling Order by date desc Limit 1'
        cursor = mydb.cursor()
        cursor.execute(sql1)
        soiling = cursor.fetchall()
        data = json.dumps({'date': soiling[0][0], 'Soiling': soiling[0][1] * 100})
        return data
    except Exception as e:
        print(e)
        return 'no data'


@app.route('/Soiling_23', methods=['POST'])
def SoilingDAS23():
    api_key = request.headers.POST('API-Key')
    if api_key != API_KEY:
        abort(401, 'Unauthorized: Invalid API key')
    try:
        mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306,
                                       database="das2_127")
        sql1 = 'SELECT date, Soiling FROM Daily_soiling Order by date desc Limit 1'
        cursor = mydb.cursor()
        cursor.execute(sql1)
        soiling = cursor.fetchall()
        data = json.dumps({'date': soiling[0][0], 'Soiling': soiling[0][1] * 100})
        return data
    except Exception as e:
        print(e)
        return 'no data'


@app.route('/Soiling_24', methods=['POST'])
def SoilingDAS24():
    api_key = request.headers.POST('API-Key')
    if api_key != API_KEY:
        abort(401, 'Unauthorized: Invalid API key')
    try:
        mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306,
                                       database="das2_149")
        sql1 = 'SELECT date, Soiling FROM Daily_soiling Order by date desc Limit 1'
        cursor = mydb.cursor()
        cursor.execute(sql1)
        soiling = cursor.fetchall()
        data = json.dumps({'date': soiling[0][0], 'Soiling': soiling[0][1] * 100})
        return data
    except Exception as e:
        print(e)
        return 'no data'


@app.route('/Soiling_25', methods=['POST'])
def SoilingDAS25():
    api_key = request.headers.POST('API-Key')
    if api_key != API_KEY:
        abort(401, 'Unauthorized: Invalid API key')
    try:
        mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306,
                                       database="das2_150")
        sql1 = 'SELECT date, Soiling FROM Daily_soiling Order by date desc Limit 1'
        cursor = mydb.cursor()
        cursor.execute(sql1)
        soiling = cursor.fetchall()
        data = json.dumps({'date': soiling[0][0], 'Soiling': soiling[0][1] * 100})
        return data
    except Exception as e:
        print(e)
        return 'no data'


@app.route('/Soiling_26', methods=['POST'])
def SoilingDAS26():
    api_key = request.headers.POST('API-Key')
    if api_key != API_KEY:
        abort(401, 'Unauthorized: Invalid API key')
    try:
        mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306,
                                       database="das2_151")
        sql1 = 'SELECT date, Soiling FROM Daily_soiling Order by date desc Limit 1'
        cursor = mydb.cursor()
        cursor.execute(sql1)
        soiling = cursor.fetchall()
        data = json.dumps({'date': soiling[0][0], 'Soiling': soiling[0][1] * 100})
        return data
    except Exception as e:
        print(e)
        return 'no data'


@app.route('/Soiling_27', methods=['POST'])
def SoilingDAS27():
    api_key = request.headers.POST('API-Key')
    if api_key != API_KEY:
        abort(401, 'Unauthorized: Invalid API key')
    try:
        mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306,
                                       database="das2_152")
        sql1 = 'SELECT date, Soiling FROM Daily_soiling Order by date desc Limit 1'
        cursor = mydb.cursor()
        cursor.execute(sql1)
        soiling = cursor.fetchall()
        data = json.dumps({'date': soiling[0][0], 'Soiling': soiling[0][1] * 100})
        return data
    except Exception as e:
        print(e)
        return 'no data'


@app.route('/Soiling_28', methods=['POST'])
def SoilingDAS28():
    api_key = request.headers.POST('API-Key')
    if api_key != API_KEY:
        abort(401, 'Unauthorized: Invalid API key')
    try:
        mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306,
                                       database="das2_153")
        sql1 = 'SELECT date, Soiling FROM Daily_soiling Order by date desc Limit 1'
        cursor = mydb.cursor()
        cursor.execute(sql1)
        soiling = cursor.fetchall()
        data = json.dumps({'date': soiling[0][0], 'Soiling': soiling[0][1] * 100})
        return data
    except Exception as e:
        print(e)
        return 'no data'


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.config['DEBUG'] = True
    app.run(host='0.0.0.0', port=8001)
