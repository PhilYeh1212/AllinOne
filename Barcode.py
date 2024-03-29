import tkinter as tk
import csv
from datetime import datetime

# 初始化掃描結果列表和計數器
scan_results = []
barcode_results=[]
csv_results=[]
scan_count = 1
adc_activated = False
today = datetime.now().strftime('%Y-%m-%d')

# 設定當達到176筆時啟動ADC
ADC_TRIGGER_COUNT = 5

def on_scan(event=None):
    global scan_count, adc_activated
    barcode = barcode_entry.get().strip()
    if barcode:
        if barcode not in barcode_results:
            # 將掃描結果添加到列表中
            count = '%s;%s'%(scan_count, barcode)
            barcode_results.append(barcode)
            scan_results.append(count)
            csv_results.append(count)
            result_text.config(state=tk.NORMAL)
            result_text.insert(tk.END, count + '\n')
            result_text.config(state=tk.DISABLED)
            barcode_entry.delete(0, tk.END)
            scan_count += 1
            if scan_count >= ADC_TRIGGER_COUNT and not adc_activated:
                # 啟動ADC
                activate_adc()
                adc_activated = True
            update_scan_display()
        else:
            barcode_entry.delete(0, tk.END)

def clear_results():
    global scan_results, scan_count, adc_activated, csv_results
    scan_results = []
    scan_count = 1
    adc_activated = False
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.config(state=tk.DISABLED)
    update_scan_display()
    
def undo():
    global scan_results, scan_count, adc_activated, csv_results
    if scan_count > 0:
        scan_results.pop()
        barcode_results.pop()
        csv_results.pop()
        scan_count -= 1
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        for result in scan_results:
            result_text.insert(tk.END, result + '\n')
        result_text.config(state=tk.DISABLED)

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
root.geometry("700x400")

# 創建條碼輸入框，並鎖定輸入列以防止點擊其他地方
barcode_entry = tk.Entry(root, width=40)
barcode_entry.pack(pady=10)

# 創建掃描結果列表框
scan_listbox = tk.Listbox(root, width=60, height=5, font=72)
scan_listbox.pack()

result_text = tk.Text(root, height=5, width=60, font=72)
result_text.pack()

# 創建清空按鈕
clear_button = tk.Button(root, text="Clear", command=clear_results, width=5, height=2)
clear_button.pack(side="left")

undo_button = tk.Button(root, text='Undo', command=undo, width=5, height=2)
undo_button.pack(side="right")

# 綁定回車鍵事件
barcode_entry.bind('<Return>', on_scan)

# 啟動Tkinter事件迴圈
root.mainloop()
