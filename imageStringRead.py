import easyocr

# 創建一個OCR讀取器
reader = easyocr.Reader(['en'])

# 開啟圖片
image_path = r"C:\Users\phil.yeh\Downloads\IMG_2095_0.jpg"

# 使用OCR讀取圖片中的文字
results = reader.readtext(image_path)

# 列印識別到的文字
for (bbox, text, prob) in results:
    print(text)