import tkinter as tk
import csv
from datetime import datetime

# 初始化掃描結果列表和計數器
scan_results = []
csv_results=[]
scan_count = 1
adc_activated = False
today = datetime.now().strftime('%Y-%m-%d')

# 設定當達到176筆時啟動ADC
ADC_TRIGGER_COUNT = 5

def on_scan(event=None):
    global scan_count, adc_activated
    barcode = barcode_entry.get()
    if barcode:
        # 將掃描結果添加到列表中
        count = '%s;%s'%(scan_count, barcode)
        scan_results.append(count)
        csv_results.append(count)
        barcode_entry.delete(0, tk.END)
        scan_count += 1
        if scan_count >= ADC_TRIGGER_COUNT and not adc_activated:
            # 啟動ADC
            activate_adc()
            adc_activated = True
        update_scan_display()

def clear_results():
    global scan_results, scan_count, adc_activated, csv_results
    scan_results = []
    scan_count = 1
    adc_activated = False
    update_scan_display()

def activate_adc():
    # 此處可以放啟動ADC的程式碼
    # 範例: print("ADC已啟動")
    pass

def update_scan_display():
    # 清空列表框
    scan_listbox.delete(0, tk.END)
    # 將掃描結果顯示在列表框中
    for result in scan_results:
        scan_listbox.insert(tk.END, result)

    # 寫入掃描結果到CSV文件
    with open('%s%s%s'%('scan_results', today, '.csv'), mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Scan Time', 'Count', 'Barcode'])
        for result in csv_results:
            writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), result])

# 創建主窗口
root = tk.Tk()
root.title("Barcode Scanner")

# 創建條碼輸入框，並鎖定輸入列以防止點擊其他地方
barcode_entry = tk.Entry(root, width=30)
barcode_entry.pack(pady=10)
barcode_entry.bind("<FocusIn>", lambda e: barcode_entry.config(state=tk.NORMAL))
barcode_entry.bind("<FocusOut>", lambda e: barcode_entry.config(state=tk.DISABLED))

# 創建掃描結果列表框
scan_listbox = tk.Listbox(root, width=40, height=10)
scan_listbox.pack()

# 創建清空按鈕
clear_button = tk.Button(root, text="Clear", command=clear_results)
clear_button.pack()

# 綁定回車鍵事件
barcode_entry.bind('<Return>', on_scan)

# 啟動Tkinter事件迴圈
root.mainloop()