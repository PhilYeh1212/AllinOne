import json
import requests

url = "http://34.80.19.148:8001/Soiling前鋒子"  # 要請求的URL

# 發送HTTP GET請求
response = requests.get(url)

# 檢查回應的狀態碼
if response.status_code == 200:
    # 請求成功，處理回應內容
    data = response.text  # 解析回應的JSON數據
    soiling = json.loads(data)
    print(soiling['Soiling'])
else:
    # 請求失敗，顯示錯誤訊息
    print("請求失敗，狀態碼：", response.status_code)