
import tkinter as tk
from threading import Thread
from turtle import color
import RPi.GPIO as GPIO # type: ignore
import serial # type: ignore
import time
import os 

RELAY_PIN1 = 26 # โซลินอยถังเพาะ
RELAY_PIN2 = 16 # มอเตอร์ถังเพาะ
RELAY_PIN3 = 20 # มอเตอร์บำบัดน้ำ
RELAY_PIN4 = 21 # มอเตอร์ถังเก็บน้ำ โซลินอยถังเก็บน้ำ
RELAY_PIN5 = 5 # พัดลม
RELAY_PIN6 = 6 # ฮีทเตอร์
RELAY_PIN7 = 13 # มอเตอร์ถังฮอร์โมน โซลินอยถังเก็บฮอร์โมน
FLOATSWITCH_PIN1 = 23 # ลูกลอยถังน้ำ บน
FLOATSWITCH_PIN2 = 24 # ลูกลอยถังน้ำ ล่าง
# FLOATSWITCH_PIN3 = 23 # ลูกลอยถังฮอร์โมน ล่าง
# FLOATSWITCH_PIN4 = 24 # ลูกลอยถังฮอร์โมน บน

class WateringSystem:

    def __init__(self, root):

        self.root = root
        self.root.title("ระบบควบคุมปัจจัยการเพาะปลูกถั่วงอก")
        self.root.option_add("*Font", "consolas 20")
        self.root.geometry('1080x720')
        self.setup_gpio()
        self.create_widgets()
        
        self.stop_flag = False
        self.start_time = None
    
    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RELAY_PIN1, GPIO.OUT)
        GPIO.setup(RELAY_PIN2, GPIO.OUT)
        GPIO.setup(RELAY_PIN3, GPIO.OUT)
        GPIO.setup(RELAY_PIN4, GPIO.OUT)
        GPIO.setup(RELAY_PIN5, GPIO.OUT)
        GPIO.setup(RELAY_PIN6, GPIO.OUT)
        GPIO.setup(RELAY_PIN7, GPIO.OUT)
        GPIO.setup(FLOATSWITCH_PIN1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(FLOATSWITCH_PIN2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # GPIO.setup(FLOATSWITCH_PIN3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # GPIO.setup(FLOATSWITCH_PIN4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    def create_widgets(self):
        
        # ส่วนบนโปรแกรม
        top_frame = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        top_frame.grid(row=0, column=0,columnspan=2, padx=10, pady=10)

        self.text = tk.Label(top_frame, text="ระบบควบคุมปัจจัยการเพาะปลูกถั่วงอก", font=("consolas", 26))
        self.text.pack(padx=3, pady=3, anchor="w")

        # ส่วนของปุ่ม
        button_frame = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        button_frame.grid(row=1, column=1, padx=5, pady=10, sticky="e")

        self.start_button = tk.Button(button_frame, text="เริ่มการเพาะปลูก  ", font=("consolas", 18), command=self.start_program)
        self.start_button.pack(padx=10, pady=10, anchor="w")

        self.stop_button = tk.Button(button_frame,  text="หยุดการเพาะปลูก ", font=("consolas", 18), command=self.stop_program)
        self.stop_button.pack(padx=10, pady=10, anchor="w")

        self.wash_button = tk.Button(button_frame,  text="ล้างระบบน้ำภายใน", font=("consolas", 18), command=self.rainwater)
        self.wash_button.pack(padx=10, pady=10, anchor="w")
        
        self.wash_button = tk.Button(button_frame,  text="ปรับค่าด้วยตัวเอง ", font=("consolas", 18), command=self.manual_value)
        self.wash_button.pack(padx=10, pady=10, anchor="w")

        self.wash_button = tk.Button(button_frame,  text="ปลูกแบบอัตโนมัติ ", font=("consolas", 18), command=self.autostart_program)
        self.wash_button.pack(padx=10, pady=10, anchor="w")

        

        self.bean_var = tk.StringVar()
        self.bean_var.set(" เลือกชนิดถั่ว ")
        self.bean_dropdown = tk.OptionMenu(button_frame, self.bean_var, "ถั่วเขียว", "ถั่วแขกดำ")
        self.bean_dropdown.config(font=("consolas", 20))
        self.bean_dropdown.pack(padx=20, pady=10, anchor="e")

        self.exit = tk.Button(button_frame, text="ออกจากโปรแกรม", font=("consolas", 20), command=self.exitprogram)
        self.exit.pack(padx=10, pady=20, anchor="w")

        # ส่วนของค่าสถานะ
        status_frame = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        status_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.timer_label = tk.Label(status_frame, text="เวลา : 0 วัน 0 ชั่วโมง 0 นาที 0 วินาที ", font=("consolas", 21))
        self.timer_label.pack(padx=15, pady=10, anchor="w")

        self.ph_label = tk.Label(status_frame, text="ความเป็น กรด-ด่าง : ", font=("consolas", 21))
        self.ph_label.pack(padx=15, pady=10, anchor="w")

        # self.sensor1_label = tk.Label(status_frame, text="ความชื้นตัวที่ 1: อุณหภูมิตัวที่ 1: ", font=("consolas", 21))
        # self.sensor1_label.pack(padx=15, pady=10, anchor="w")

        # self.sensor2_label = tk.Label(status_frame, text="ความชื้นตัวที่ 2: อุณหภูมิตัวที่ 2: ", font=("consolas", 21))
        # self.sensor2_label.pack(padx=15, pady=10, anchor="w")

        self.avg_label = tk.Label(status_frame, text="ความชื้นเฉลี่ย: อุณหภูมิเฉลี่ย: ", font=("consolas", 21))
        self.avg_label.pack(padx=15, pady=10, anchor="w")

        self.flow_label = tk.Label(status_frame, text="อัตตราการไหลของน้ำ: ", font=("consolas", 21))
        self.flow_label.pack(padx=15, pady=10, anchor="w")

        self.water_temp = tk.Label(status_frame, text="อุณหภูมิในน้ำ : ", font=("consolas", 21))
        self.water_temp.pack(padx=15, pady=10, anchor="w")

        self.status = tk.Label(status_frame, text="สถานะการทำงาน : ", font=("consolas", 21))
        self.status.pack(padx=15, pady=10, anchor="w")

        self.status1 = tk.Label(status_frame, text="ระดับน้ำในถัง : ", font=("consolas", 21))
        self.status1.pack(padx=15, pady=10, anchor="w")

        self.update_data()
    
    def update_timer(self):
        if self.start_time is not None:
            elapsed_time = time.time() - self.start_time
            days, remainder = divmod(elapsed_time, 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_string = "เวลา : {:01} วัน {:01} ชั่วโมง {:01} นาที {:01} วินาที".format(int(days), int(hours), int(minutes), int(seconds))
            self.timer_label.config(text=time_string)
        self.root.after(1000, self.update_timer)

        if days == 4:
            self.cleanup_gpio()
            self.stop_program()

    def watercheck(self):
        while True:
            pin1_state = GPIO.input(FLOATSWITCH_PIN1)
            pin2_state = GPIO.input(FLOATSWITCH_PIN2)

            if pin1_state == GPIO.LOW and pin2_state == GPIO.LOW:
                GPIO.output(RELAY_PIN3, GPIO.HIGH)
                GPIO.output(RELAY_PIN3, GPIO.HIGH)
                print("ระดับน้ำในถังต่ำเกินไป กำลังเติมน้ำ")
                time.sleep(1)

                while pin1_state == GPIO.LOW and pin2_state == GPIO.HIGH:
                    GPIO.output(RELAY_PIN3, GPIO.HIGH)
                    print("ระดับน้ำในถังกำลังดี กำลังเติมน้ำ")
                    time.sleep(1)
                    
            elif pin1_state == GPIO.HIGH and pin2_state == GPIO.HIGH:
                GPIO.output(RELAY_PIN3, GPIO.LOW)
                print("น้ำเต็มถังแล้วโว้ย!!")
                time.sleep(1)

    def run_program(self):
        self.start_time = time.time()
        
        try:
            while True:
                # GPIO.output(RELAY_PIN1, GPIO.HIGH)
                GPIO.output(RELAY_PIN2, GPIO.HIGH)
                # GPIO.output(RELAY_PIN4, GPIO.HIGH)
                print("กำลังรดน้ำ")
                time.sleep(timW*60)

                # GPIO.output(RELAY_PIN1, GPIO.LOW)
                GPIO.output(RELAY_PIN2, GPIO.LOW)
                # GPIO.output(RELAY_PIN4, GPIO.LOW)
                print("หยุดการให้น้ำ")
                time.sleep(1)

                # GPIO.output(RELAY_PIN5, GPIO.HIGH)
                # print("พัดลมระบายอากาศ กำลังทำงาน")
                # time.sleep(timfanW*60)

                # GPIO.output(RELAY_PIN5, GPIO.LOW)
                # print("พัดลมระบายอากาศ หยุดทำงาน")
                # time.sleep(1)

        except KeyboardInterrupt:
            self.cleanup_gpio()
    
    def start_program(self):
        variable12 = "กำลังทำการเพาะปลูก"
        if self.bean_var.get() == "เลือกชนิดถั่ว":
        # ให้แสดงข้อความให้ผู้ใช้เลือกชนิดถั่วก่อน
            tk.messagebox.showinfo("แจ้งเตือน", "กรุณาเลือกชนิดถั่วก่อนที่จะเริ่มโปรแกรมการเพาะปลูก")

        elif self.bean_var.get() == "ถั่วเขียว" or self.bean_var.get() == "ถั่วแขกดำ":
        # เมื่อผู้ใช้เลือกชนิดถั่วแล้ว ให้เริ่มโปรแกรม
            self.stop_flag = False
            self.program_thread = Thread(target=self.run_program)
            self.program_thread.start()
            self.program_thread = Thread(target=self.watercheck)
            self.program_thread.start()
            # self.program_thread = Thread(target=self.tempwater)
            # self.program_thread.start()
            self.status1.config(text="ประเภทการทำงาน :  {:s} ".format(variable12))
            self.update_timer()
            
    def autostart_program(self):
        global temH, temL, timW, timfanW
        temH = 36
        temL = 32
        timW = 10
        timfanW = 20

        variable12 = "กำลังทำการเพาะปลูก"
        confirm = tk.messagebox.asquestion("ยืนยัน", "เมื่อกดยืนยันแล้ว จะเริ่มปลูกทันที")
        if confirm == "yes":
        # ให้แสดงข้อความให้ผู้ใช้เลือกชนิดถั่วก่อน
            if self.bean_var.get() == "เลือกชนิดถั่ว":
                tk.messagebox.showinfo("แจ้งเตือน", "กรุณาเลือกชนิดถั่วก่อนที่จะเริ่มโปรแกรมการเพาะปลูก")
            elif self.bean_var.get() == "ถั่วเขียว" or self.bean_var.get() == "ถั่วแขกดำ":
            # เมื่อผู้ใช้เลือกชนิดถั่วแล้ว ให้เริ่มโปรแกรม
                self.stop_flag = False
                self.program_thread = Thread(target=self.run_program)
                self.program_thread.start()
                self.program_thread = Thread(target=self.watercheck)
                self.program_thread.start()
                self.program_thread = Thread(target=self.tempwater)
                self.program_thread.start()
                self.status1.config(text="ประเภทการทำงาน :  {:s} ".format(variable12))
                self.update_timer()
        else:
            pass

    def stop_program(self):
        self.stop_flag = True
        if self.program_thread is not None and self.program_thread.is_alive():
            self.program_thread.join()
        self.cleanup_gpio()

    def cleanup_gpio(self):
        GPIO.cleanup()
        
    def update_data(self):
        ser = serial.Serial('/dev/ttyUSB0', 9600)
        data = ser.readline().decode().strip()
        values = data.split(',')
        variable1 = float(values[0])
        # variable2 = float(values[1])
        # variable3 = float(values[2])
        # variable4 = float(values[3])
        # variable5 = float(values[4])
        variable6 = float(values[1])
        variable7 = float(values[2])
        # variable8 = float(values[7])
        variable9 = float(values[3])
        variable10 = float(values[4])
        variable11 = "พร้อมใช้งาน"
        

        self.ph_label.config(text="ความเป็น กรด-ด่าง : {:.2f} Ph".format(variable1))
        # self.sensor1_label.config(text="ความชื้นตัวที่ 1: {:.2f}%  อุณหภูมิตัวที่ 1: {:.2f} °C".format(variable2, variable3))
        # self.sensor2_label.config(text="ความชื้นตัวที่ 2: {:.2f}%  อุณหภูมิตัวที่ 2: {:.2f} °C".format(variable4, variable5))
        self.avg_label.config(text="ความชื้นเฉลี่ย: {:.2f}%  อุณหภูมิเฉลี่ย: {:.2f} °C".format(variable6, variable7))
        self.flow_label.config(text="อัตตราการไหลของน้ำ: {:.2f} ลิตร/นาที".format(variable9/10))
        self.water_temp.config(text="อุณหภูมิในน้ำ :  {:.2f} °C".format(variable10))
        self.status.config(text="สถานะการทำงาน :  {:s} ".format(variable11))
        
        self.root.after(1000, self.update_data)

    def rainwater(self):
        self.start_time = time.time()
        self.stop_flag = False
        self.program_thread = Thread(target=self.run_program)
        self.program_thread.start()
        self.program_thread = Thread(target=self.watercheck)
        self.program_thread.start()
        self.update_timer()

    # def tempwater(self):
    #     while True:
    #         if  int(self.water_temp) < int(temL) :
    #             GPIO.output(RELAY_PIN6, GPIO.HIGH)
    #             time.sleep(1)
    #             while int(self.water_temp) > int(temL) or int(self.water_temp) < int(temH) :
    #                 GPIO.output(RELAY_PIN6, GPIO.HIGH)
    #                 time.sleep(1)
    #         elif int(self.water_temp) > int(temH):
    #             GPIO.output(RELAY_PIN6, GPIO.LOW)
    #             time.sleep(1) 
        

    def manual_value(self):    

        def save_values():
            global temH, temL, timW, timfanW
            temH = int(entry_temH.get())
            temL = int(entry_temL.get())
            timW = int(entry_timW.get())
            timfanW = int(entry_timfanW.get())
            tk.messagebox.showinfo("แจ้งเตือน", "บันทักค่าเรียบร้อยแล้ว !! ")
            print_values()

        def print_values():
            print("Temperature High (temH):", temH)
            print("Temperature Low (temL):", temL)
            print("Time Weight (timW):", timW)
            print("Time Weight (timW):", timfanW)

        def increase_value(entry):
            current_value = int(entry.get())
            entry.delete(0, tk.END)
            entry.insert(0, str(current_value + 1))

        def decrease_value(entry):
            current_value = int(entry.get())
            entry.delete(0, tk.END)
            entry.insert(0, str(current_value - 1))

        
        # สร้างหน้าต่าง
        root1 = tk.Tk()
        root1.title("กำหนดค่าด้วยตัวเอง")
        root1.geometry("800x380+130+100")


        # สร้าง Entry สำหรับรับค่า และตั้งค่าเริ่มต้นเป็น 0
        entry_temH = tk.Entry(root1)
        entry_temL = tk.Entry(root1)
        entry_timW = tk.Entry(root1)
        entry_timfanW = tk.Entry(root1)

        entry_temH.insert(0, "36")
        entry_temL.insert(0, "32")
        entry_timW.insert(0, "12")
        # entry_timfanW.insert(0, "18")

        # ตำแหน่ง Entry ในหน้าต่าง
        entry_temH.grid(row=0, column=1)
        entry_temL.grid(row=1, column=1)
        entry_timW.grid(row=2, column=1)
        entry_timfanW.grid(row=3, column=1)

        # ปุ่มเพิ่มและลบตัวเลข
        increase_button_temH = tk.Button(root1, text="+", font=("consolas", 22), command=lambda: increase_value(entry_temH))
        decrease_button_temH = tk.Button(root1, text="-", font=("consolas", 22), command=lambda: decrease_value(entry_temH))
        increase_button_temL = tk.Button(root1, text="+", font=("consolas", 22), command=lambda: increase_value(entry_temL))
        decrease_button_temL = tk.Button(root1, text="-", font=("consolas", 22), command=lambda: decrease_value(entry_temL))
        increase_button_timW = tk.Button(root1, text="+", font=("consolas", 22), command=lambda: increase_value(entry_timW))
        decrease_button_timW = tk.Button(root1, text="-", font=("consolas", 22), command=lambda: decrease_value(entry_timW))
        increase_button_timfanW = tk.Button(root1, text="+", font=("consolas", 22), command=lambda: increase_value(entry_timfanW))
        decrease_button_timfanW = tk.Button(root1, text="-", font=("consolas", 22), command=lambda: decrease_value(entry_timfanW))

        # ตำแหน่งปุ่มในหน้าต่าง
        increase_button_temH.grid(row=0, column=2)
        decrease_button_temH.grid(row=0, column=3)
        increase_button_temL.grid(row=1, column=2)
        decrease_button_temL.grid(row=1, column=3)
        increase_button_timW.grid(row=2, column=2)
        decrease_button_timW.grid(row=2, column=3)
        increase_button_timfanW.grid(row=3, column=2)
        decrease_button_timfanW.grid(row=3, column=3)

        # ปุ่มบันทึกค่า
        save_button = tk.Button(root1, text="Save", font=("consolas", 22), command=save_values)
        save_button.grid(row=4, column=1,padx=10,pady=10)

        # ปุ่มปิดหน้าต่าง
        exit_button = tk.Button(root1, text="Exit", font=("consolas", 22), command=root1.destroy)
        exit_button.grid(row=5, column=1,padx=10,pady=10)

        # Label สำหรับตัวแปร
        label_temH = tk.Label(root1,    text="อุณหภูมิน้ำมากสุด (ทำการหยุดต้ม):", font=("consolas", 22))
        label_temL = tk.Label(root1,    text="อุณหภูมิน้ำต่ำ (ทำการต้มน้ำ):", font=("consolas", 22))
        label_timW = tk.Label(root1,    text="เวลามอเตอร์ให้น้ำทำงาน :", font=("consolas", 22))
        label_timfanW = tk.Label(root1, text="เวลาพักมอเตอร์ให้น้ำ :", font=("consolas", 22))

        # ตำแหน่ง Label ในหน้าต่าง
        label_temH.grid(row=0, column=0)
        label_temL.grid(row=1, column=0)
        label_timW.grid(row=2, column=0)
        label_timfanW.grid(row=3, column=0)

# เริ่มการทำงานของโปรแกรม
    def exitprogram(self):
        self.cleanup_gpio()
        root.destroy()
        os.system("sudo shutdown -h now")


root = tk.Tk()
app1 = WateringSystem(root)
root.mainloop()

