import mysql.connector

# MySQL 服务器连接信息
mysql_config = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "Oerlikon;1234"
}

try:
    # 連接到 MySQL 伺服器
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()

    # 取得所有資料庫名稱
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()

    # 遍歷每個資料庫並執行查詢操作
    for db_info in databases:
        db_name = db_info[0]

        # 重新連接到目前的資料庫
        db_config = {
            "host": mysql_config["host"],
            "user": mysql_config["user"],
            "password": mysql_config["password"],
            "database": db_name
        }

        try:
            conn_db = mysql.connector.connect(**db_config)
            cursor_db = conn_db.cursor()

            # 檢查是否存在 T2_inv 表
            cursor_db.execute("SHOW TABLES LIKE 'T2_inv'")
            table_exists = cursor_db.fetchone()

            if table_exists:
                # 執行查詢操作
                select_query = """
                SELECT INVXX07, daq_date
                FROM T2_inv
                where INVXX07 > 1000 and DAQ_Date = '2023/10/16'
                """
                cursor_db.execute(select_query)
                result = cursor_db.fetchall()

                # 處理查詢結果，只顯示一次資料庫名稱
                if result:
                    print(f"資料庫：{db_name}+{result} - 存在重複記錄")

            cursor_db.close()
            conn_db.close()

        except mysql.connector.Error as db_err:
            print(f"在資料庫 {db_name} 中發生錯誤: {db_err}")
            continue  # 繼續處理下一個資料庫

except mysql.connector.Error as err:
    print(f"在連接到MySQL伺服器時發生錯誤: {err}")

finally:
    cursor.close()