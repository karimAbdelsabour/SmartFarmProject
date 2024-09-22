#include <dht11.h>

#define DHT11PIN 2                   // Pin for DHT11 sensor
#define MOTOR_PIN 9                  // Pin connected to the DC motor
#define FLAME_SENSOR_PIN 3           // Pin connected to the flame sensor
#define MOISTURE_SENSOR_PIN A2       // Pin for the moisture sensor
#define RAIN_LEVEL_PIN A0            // Pin connected to the rain level sensor
#define LDR_PIN A1                   // Pin for the LDR sensor

// Thresholds and constants
#define NUM_READINGS 10              // Number of readings for average
#define RAIN_LEVEL_THRESHOLD 50       // Rain level threshold percentage
#define MOISTURE_THRESHOLD 20         // Moisture sensor threshold
#define MAX_SENSOR_READING 1023       // Maximum sensor reading for 10-bit ADC

dht11 DHT11;

void setup() {
  Serial.begin(9600);
  pinMode(MOTOR_PIN, OUTPUT);         // Set motor pin as output
  pinMode(FLAME_SENSOR_PIN, INPUT);   // Set flame sensor pin as input
  digitalWrite(MOTOR_PIN, LOW);       // Ensure the motor is off initially
}

void loop() {
  // Read flame sensor
  int flameSensorValue = digitalRead(FLAME_SENSOR_PIN);
  
  // Read temperature and humidity from DHT11
  int chk = DHT11.read(DHT11PIN);
  
  // Read rain level sensor
  long total = 0; 
  for (int i = 0; i < NUM_READINGS; i++) {
    total += analogRead(RAIN_LEVEL_PIN);
    delay(100); 
  }
  int averageRainReading = total / NUM_READINGS;
  int rainLevelPercentage = map(averageRainReading, 0, MAX_SENSOR_READING, 0, 100);
  rainLevelPercentage = constrain(rainLevelPercentage, 0, 100);

  // Read moisture sensor
  int moistureValue = analogRead(MOISTURE_SENSOR_PIN);
  int moisturePercentage = map(moistureValue, 0, MAX_SENSOR_READING, 100, 0);
  moisturePercentage = constrain(moisturePercentage, 0, 100);

  // Read LDR sensor as an analog value
  int ldrValue = analogRead(LDR_PIN);
  
  // Send data in the specified format
  Serial.print("Moisture Level, ");
  Serial.println(moisturePercentage);
  
  Serial.print("Flame, ");
  Serial.println(flameSensorValue == LOW ? '1' : '0');
  
  Serial.print("Humidity, ");
  Serial.println((float)DHT11.humidity, 2);
  
  Serial.print("Temperature, ");
  Serial.println((float)DHT11.temperature, 2);
  
  Serial.print("Rain Level, ");
  Serial.println(rainLevelPercentage);
  
  Serial.print("LDR, ");
  Serial.println(ldrValue); // Send LDR value as analog reading

  delay(2000); // Delay before the next loop iteration
}
