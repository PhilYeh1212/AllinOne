import easyocr
import csv
import os
import time

# 指定图像文件夹路径
image_folder = r"C:\_Phil\04_Python\Barcode"

# 指定CSV文件名
csv_filename = r"C:\_Phil\04_Python\Barcode\output.csv"

# 初始化CSV文件，写入表头
with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['Image File', 'Text']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

# 初始化easyocr识别器
reader = easyocr.Reader(['en'])  # 您可以更改语言

# 循环处理每个图像文件
for filename in os.listdir(image_folder):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        image_path = os.path.join(image_folder, filename)
        try:
            # 使用easyocr进行文本提取
            results = reader.readtext(image_path)

            # 提取识别结果并写入CSV文件
            with open(csv_filename, mode='a', newline='', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                for (bbox, text, prob) in results:
                    writer.writerow({'Image File': filename, 'Text': text})
                    time.sleep(0.0001)
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")

print("Text extraction complete. Results saved to", csv_filename)