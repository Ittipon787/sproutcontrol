import tkinter as tk
from tkinter import messagebox

def calculate_total():
    try:
        primary_money = float(entry_money.get())
        lineman_vat = 0.3
        vat = 0.07

        ans = primary_money - (primary_money * lineman_vat)
        total = ans - (ans * vat)

        label_result.config(text=f"\u0e23\u0e27\u0e21\u0e40\u0e07\u0e34\u0e19\u0e23\u0e27\u0e21\u0e21\u0e35\u0e20\u0e32\u0e29\u0e35 (\u0e1a\u0e27\u0e01 VAT): {total:.2f}")
    except ValueError:
        messagebox.showerror("Error", "\u0e01\u0e23\u0e38\u0e13\u0e32\u0e23\u0e30\u0e1a\u0e38\u0e1b\u0e08\u0e33\u0e19\u0e27\u0e19\u0e40\u0e1b\u0e47\u0e19\u0e15\u0e31\u0e27\u0e40\u0e25\u0e02\u0e02\u0e2d\u0e07\u0e40\u0e25\u0e02\u0e17\u0e35\u0e48\u0e16\u0e39\u0e01\u0e15\u0e49\u0e19")

# สร้างหน้าต่างหลัก
root = tk.Tk()
root.title("VAT Calculator")
root.geometry("400x200")

# สร้าง Label และ Entry สำหรับป้อนจำนวนเงิน
label_prompt = tk.Label(root, text="\u0e23\u0e30\u0e1a\u0e38\u0e08\u0e33\u0e19\u0e27\u0e19\u0e40\u0e1b\u0e47\u0e19\u0e15\u0e49\u0e19: ")
label_prompt.pack(pady=10)

entry_money = tk.Entry(root, width=20)
entry_money.pack(pady=5)

# ปุ่มสำหรับคำนวณ
button_calculate = tk.Button(root, text="\u0e04\u0e33\u0e19\u0e27\u0e13", command=calculate_total)
button_calculate.pack(pady=10)

# แสดงผลลัพธ์
label_result = tk.Label(root, text="", fg="blue")
label_result.pack(pady=10)

# เริ่มต้นโปรแกรม
root.mainloop()