#include <OneWire.h>
#include <DallasTemperature.h>
#include <DHT.h>

// ------------------------ DS18B20 ------------------------ //
// Pin ที่เชื่อม DATA ของ DS18B20
#define ONE_WIRE_BUS 48
// ตั้งค่า OneWire instance
OneWire oneWire(ONE_WIRE_BUS);
// ตั้งค่า DallasTemperature library instance
DallasTemperature sensors(&oneWire);

// ------------------------ DHT22 ------------------------ //
// พินสำหรับเซ็นเซอร์ DHT22
#define DHTPIN1 49 // พินสำหรับเซ็นเซอร์ DHT22 ตัวที่ 1
#define DHTPIN2 47 // พินสำหรับเซ็นเซอร์ DHT22 ตัวที่ 2
// ระบุประเภทเซ็นเซอร์
#define DHTTYPE DHT22
// สร้างอินสแตนซ์สำหรับ DHT22
DHT dht1(DHTPIN1, DHTTYPE);
DHT dht2(DHTPIN2, DHTTYPE);

void setup() {
  Serial.begin(9600);
  
  // เริ่มต้น DS18B20
  Serial.println("Initializing DS18B20...");
  sensors.begin();
  
  // เริ่มต้น DHT22
  Serial.println("Initializing DHT22 sensors...");
  dht1.begin();
  dht2.begin();
}

void loop() {
  // ------------------------ DS18B20 ------------------------ //
  // ขอข้อมูลอุณหภูมิจาก DS18B20
  sensors.requestTemperatures();
  float temperatureC = sensors.getTempCByIndex(0);

  // แสดงผลอุณหภูมิจาก DS18B20
  Serial.println("--- DS18B20 ---");
  Serial.print("Temperature (°C): ");
  Serial.println(temperatureC);

  // ------------------------ DHT22 ตัวที่ 1 ------------------------ //
  float humidity1 = dht1.readHumidity();
  float temperatureDHT1 = dht1.readTemperature();

  // ตรวจสอบค่าจาก DHT22 ตัวที่ 1
  if (isnan(humidity1) || isnan(temperatureDHT1)) {
    Serial.println("Failed to read from DHT22 sensor 1!");
  } else {
    Serial.println("--- DHT22 Sensor 1 ---");
    Serial.print("Humidity: ");
    Serial.print(humidity1);
    Serial.print("%\tTemperature: ");
    Serial.print(temperatureDHT1);
    Serial.println("°C");
  }

  // ------------------------ DHT22 ตัวที่ 2 ------------------------ //
  float humidity2 = dht2.readHumidity();
  float temperatureDHT2 = dht2.readTemperature();

  // ตรวจสอบค่าจาก DHT22 ตัวที่ 2
  if (isnan(humidity2) || isnan(temperatureDHT2)) {
    Serial.println("Failed to read from DHT22 sensor 2!");
  } else {
    Serial.println("--- DHT22 Sensor 2 ---");
    Serial.print("Humidity: ");
    Serial.print(humidity2);
    Serial.print("%\tTemperature: ");
    Serial.print(temperatureDHT2);
    Serial.println("°C");
  }

  // หน่วงเวลา 2 วินาที
  delay(2000);
   Serial.print("\n\n\n");
}
