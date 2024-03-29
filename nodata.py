import mysql.connector
from datetime import datetime

host = '35.236.181.75'
user = 'root'
password = 'Oerlikon;1234'

skip_databases = ['FSLG_FS200700401','FSLG_FS200700402','FSLG_TW190980', 'FSLG_TW150498', 'FSLG_FS2003002', 'FSLG_TW211073','FS_Logger_site0_XXX','FSLG_TW201043', 'FSLG_overview']

connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password
)

cursor = connection.cursor()

try:
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()

    for db in databases:
        db_name = db[0]

        if db_name in skip_databases:
            continue

        connection.database = db_name

        cursor.execute(f"SHOW TABLES IN {db_name}")
        tables = cursor.fetchall()

        if ('T2_inv',) not in tables:
            continue

        if ('T1_head',) in tables:
            today = datetime.now().strftime('%Y/%m/%d')
            query = f"SELECT * FROM {db_name}.T1_head WHERE DAQ_Date= '{today}' and DAQ_Time >= '06:00:00' and DAQ_Time <= '07:59:00'"
            query1 = f"SELECT * FROM {db_name}.T2_inv WHERE DAQ_Date= '{today}' and DAQ_Time >= '06:00:00' and DAQ_Time <= '07:59:00'"
            
            cursor.execute(query)
            results = cursor.fetchall()

            cursor.execute(query1)
            results1 = cursor.fetchall()  

            if not results and not results1:
                print(f"在資料庫 '{db_name}' 中，沒有資料。")

except mysql.connector.Error as err:
    print(f"錯誤：{err}")

finally:
    cursor.close()
    connection.close()
