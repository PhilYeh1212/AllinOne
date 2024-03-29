import pymysql

connection = pymysql.connect(host='35.236.181.75',
                             user='root',
                             password='Oerlikon;1234',
                             db='das2_fs_download')

mycursor = connection.cursor()

# 刪除das_XX_download表中的前59條記錄
delete_sql = "DELETE FROM all_das2_solling ORDER BY date DESC LIMIT 59"
mycursor.execute(delete_sql)

# 提取das_XX_download_bk表中最新的60條記錄
mycursor.execute("SELECT * FROM Fs_all_das2_solling ORDER BY date DESC LIMIT 60")
myresult = mycursor.fetchall()

for row in myresult:
    #print(row)  # 印出CSV文件的內容

    # 插入行數據到MySQL表中
    sql = "INSERT INTO all_das2_solling (Date, das2_30, das2_31, das2_37, das2_48, das2_76, das2_77, das2_78, das2_79, das2_80, das2_81, das2_85, das2_86, das2_87, das2_88, das2_89, das2_90, das2_91, das2_92, das2_93, das2_94, das2_115, das2_116, das2_117, das2_118, das2_119) VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s)"
    val = row
    print("插入資料：", val)
    mycursor.execute(sql, val)
    connection.commit()

connection.close()