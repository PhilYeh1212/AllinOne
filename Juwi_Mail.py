import pymysql
import smtplib
from email.mime.text import MIMEText

# 資料庫連線資訊
db_host = '35.221.247.182'
db_user = 'root'
db_password = 'Oerlikon;1234'
db_database = 'juwi_001_dds'

# 電子郵件配置資訊
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_user = 'sam.chan@extelenergy.com'
smtp_password = 'Sadd90551'
recipient_emails = ['sam.chan@extelenergy.com', 'billy.gan@extelenergy.com', 'phil.yeh@extelenergy.com']#,
                    #'kotaro.iwasaki@juwishizenenergy.net']

# 連接資料庫
db = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_database)
cursor = db.cursor()

# 查詢資料庫
query = "SELECT Water_Tank_Level FROM dds_rawdata WHERE TIME(Time) >= '07:00:00' AND TIME(Time) <= '07:01:00' AND Water_Tank_Level < 36"
cursor.execute(query)
result = cursor.fetchone()

# 檢查查詢結果
if result:
    # 發送電子郵件通知
    subject = "PEK Sano - DAS 給水タンクのレベルが 20 未満です"
    message = "タンクの水は20cm以下になっています。パネルの洗浄に影響が出るので、水の補充をお願いします。"

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = smtp_user
    msg['To'] = ", ".join(recipient_emails)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, recipient_emails, msg.as_string())
        print("電子郵件通知已發送")
        server.quit()
    except Exception as e:
        print("發送電子郵件失敗:", str(e))
else:
    print("水箱水位正常")

# 關閉資料庫連線
db.close()