import tkinter as tk
import RPi.GPIO as GPIO # type: ignore

# กำหนดหมายเลข GPIO ที่จะใช้สำหรับแต่ละพอร์ต
GPIO_PINS = [25, 27, 28, 29, 21, 22, 23, 26, 1, 0, 2, 3]

# การตั้งค่า GPIO
GPIO.setmode(GPIO.BCM)  # ใช้หมายเลขขาแบบ BCM
GPIO.setup(GPIO_PINS, GPIO.OUT, initial=GPIO.LOW)  # กำหนดให้ทุกพอร์ตเป็น OUTPUT และเริ่มต้นปิด

# สร้างคลาสสำหรับควบคุมสถานะรีเลย์
class RelayControllerApp:
    def __init__(self, root, num_relays):
        self.root = root
        self.num_relays = num_relays
        self.relay_states = [False] * num_relays  # เก็บสถานะของรีเลย์ (เริ่มต้นปิดทั้งหมด)

        # สร้างปุ่มแต่ละปุ่ม
        self.buttons = []
        for i in range(self.num_relays):
            btn = tk.Button(
                root, 
                text=f"Relay {i + 1} (OFF)", 
                bg="red", 
                command=lambda i=i: self.toggle_relay(i)
            )
            btn.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            self.buttons.append(btn)

    def toggle_relay(self, relay_number):
        # สลับสถานะรีเลย์
        self.relay_states[relay_number] = not self.relay_states[relay_number]
        state = self.relay_states[relay_number]
        gpio_pin = GPIO_PINS[relay_number]

        # สลับสถานะของ GPIO
        GPIO.output(gpio_pin, GPIO.HIGH if state else GPIO.LOW)

        # อัปเดตปุ่ม
        state_text = "ON" if state else "OFF"
        color = "green" if state else "red"
        self.buttons[relay_number].config(text=f"Relay {relay_number + 1} ({state_text})", bg=color)

        # พิมพ์สถานะปัจจุบัน
        print(f"Relay {relay_number + 1} (GPIO {gpio_pin}) is now {state_text}")

# สร้างหน้าต่างหลัก
root = tk.Tk()
root.title("Relay Controller")

# ตั้งค่าขนาดหน้าต่าง 1920x1080
root.geometry("1920x1080")

# สร้างโปรแกรมควบคุมรีเลย์
app = RelayControllerApp(root, num_relays=len(GPIO_PINS))

# เริ่มต้นโปรแกรม
try:
    root.mainloop()
finally:
    # ทำความสะอาด GPIO เมื่อโปรแกรมปิด
    GPIO.cleanup()
