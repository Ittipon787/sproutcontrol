import tkinter as tk
from tkinter import messagebox

def calculate_sum():
    try:
        vari1 = int(entry1.get())
        vari2 = int(entry2.get())
        vari3 = int(entry3.get())

        # คำนวณผลลัพธ์
        sum_value = vari3 - (vari1 // 3) + (vari2 // 3)

        # แสดงผลลัพธ์
        result_label.config(text=f"Sum is: {sum_value}")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid integers!")

# สร้างหน้าต่างหลัก
root = tk.Tk()
root.title("Sum Calculator")

# เพิ่ม label และ entry สำหรับ choice 1
label1 = tk.Label(root, text="Choice 1:")
label1.pack(pady=5)
entry1 = tk.Entry(root)
entry1.pack(pady=5)

# เพิ่ม label และ entry สำหรับ choice 2
label2 = tk.Label(root, text="Choice 2:")
label2.pack(pady=5)
entry2 = tk.Entry(root)
entry2.pack(pady=5)

# เพิ่ม label และ entry สำหรับ choice 3
label3 = tk.Label(root, text="Choice 3:")
label3.pack(pady=5)
entry3 = tk.Entry(root)
entry3.pack(pady=5)

# ปุ่มคำนวณ
calc_button = tk.Button(root, text="Calculate", command=calculate_sum)
calc_button.pack(pady=10)

# Label สำหรับแสดงผลลัพธ์
result_label = tk.Label(root, text="Sum is: ")
result_label.pack(pady=5)

# เริ่มโปรแกรม
root.mainloop()
