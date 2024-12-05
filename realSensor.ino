#include <DHT.h>

#define SensorPin A0   //pH meter Analog output to Arduino Analog Input 0
#define Offset 0.00    //deviation compensate
#define DHTPIN1 34     // เซ็นเซอร์ DHT หมายเลข 1 ต่อกับขา 2 ของ Arduino
#define DHTPIN2 36     // เซ็นเซอร์ DHT หมายเลข 2 ต่อกับขา 3 ของ Arduino
#define DHTTYPE DHT22  // เลือกประเภทของ DHT เป็น DHT22
#define flow_sensor 9

DHT dht1(DHTPIN1, DHTTYPE);  // สร้างอ็อบเจ็กต์ DHT สำหรับเซ็นเซอร์ DHT หมายเลข 1
DHT dht2(DHTPIN2, DHTTYPE);  // สร้างอ็อบเจ็กต์ DHT สำหรับเซ็นเซอร์ DHT หมายเลข 2
unsigned long int avgValue;

void setup() {
  Serial.begin(9600);  // เริ่มการสื่อสารผ่าน Serial Monitor
  Serial.println("DHT22 testing!");
  pinMode(flow_sensor, INPUT);
  dht1.begin();  // เริ่มต้นใช้งานเซ็นเซอร์ DHT หมายเลข 1
  dht2.begin();  // เริ่มต้นใช้งานเซ็นเซอร์ DHT หมายเลข 2
}

void loop() {

  int buf[10];                  //buffer for read analog
  for (int i = 0; i < 10; i++)  //Get 10 sample value from the sensor for smooth the value
  {
    buf[i] = analogRead(SensorPin);
    delay(10);
  }
  for (int i = 0; i < 9; i++)  //sort the analog from small to large
  {
    for (int j = i + 1; j < 10; j++) {
      if (buf[i] > buf[j]) {
        int temp = buf[i];
        buf[i] = buf[j];
        buf[j] = temp;
      }
    }
  }
  avgValue = 0;
  for (int i = 2; i < 8; i++) {
    avgValue += buf[i];
  }  //take the average value of 6 center sample

  float phValue = (float)avgValue * 5.0 / 1024 / 6;  //convert the analog into millivolt
  phValue = 3.5 * phValue + Offset;

  // อ่านค่าอุณหภูมิและความชื้นจากเซ็นเซอร์ DHT หมายเลข 1
  float h1 = dht1.readHumidity();
  float t1 = dht1.readTemperature();

  // อ่านค่าอุณหภูมิและความชื้นจากเซ็นเซอร์ DHT หมายเลข 2
  float h2 = dht2.readHumidity();
  float t2 = dht2.readTemperature();

  // ตรวจสอบว่าการอ่านค่าเซ็นเซอร์สำเร็จหรือไม่
  if (isnan(h1) || isnan(t1) || isnan(h2) || isnan(t2)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }
  uint32_t pulse = pulseIn(flow_sensor,HIGH);
  float Hz = 1 / (2 * pulse * pow(10, -6));
  float flow = 7.2725 * (float)Hz + 3.2094;
  // แสดงค่าอุณหภูมิและความชื้นจากเซ็นเซอร์ DHT ทั้งสองตัวใน Serial Monitor
  Serial.print("    ค่า pH:");
  Serial.print(phValue, 2);

  Serial.print(Hz);
  Serial.print("Hz\t");
  Serial.print(flow / 60);
  Serial.println(" L/minute");

  Serial.print("DHT1 Humidity: ");
  Serial.print(h1);
  Serial.print(" %\t");
  Serial.print("Temperature: ");
  Serial.print(t1);
  Serial.println(" *C");
  Serial.print(" \n\n");
  Serial.print("DHT2 Humidity: ");
  Serial.print(h2);
  Serial.print(" %\t");
  Serial.print("Temperature: ");
  Serial.print(t2);
  Serial.println(" *C");

  delay(2000);  // หน่วงเวลา 2 วินาทีระหว่างการอ่านค่าเซ็นเซอร์
}