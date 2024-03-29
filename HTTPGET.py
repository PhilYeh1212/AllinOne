import json
import time
import requests

url = "http://34.80.19.148:8001/Soiling_08"  # 要請求的URL
lastTi = 0
# 發送HTTP GET請求
data = 'helloWorld'

api_key = 'sa0u5U4rTTprOVtReJQKXlsAYy7Oihr3'

headers = {
    'API-Key': api_key,
    'Content-Type': 'application/json'  # 根据实际情况设置Content-Type
}

while True:
    inTi = time.time()
    if inTi - lastTi >= 5:
        response = requests.post(url, headers=headers)
        # 檢查回應的狀態碼
        if response.status_code == 200:
            # 請求成功，處理回應內容
            data = response.text  # 解析回應的JSON數據
            soiling = json.loads(data)
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), soiling)
        else:
            # 請求失敗，顯示錯誤訊息
            print("請求失敗，狀態碼：", response.status_code)
        lastTi = time.time()