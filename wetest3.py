import time
import paho.mqtt.client as paho
import serial
import ssl
import json
from gpiozero import OutputDevice, LED

# Set up GPIO pins
PUMP_PIN = 22
FAN_PIN = 27
BUZZER_PIN = 26
LED_PINS = [18, 23, 24, 25, 17]

# Initialize devices
pump = OutputDevice(PUMP_PIN)
fan = OutputDevice(FAN_PIN)
buzzer = OutputDevice(BUZZER_PIN)
leds = [LED(pin) for pin in LED_PINS]

# Set up the serial connection (adjust as needed)
ser = serial.Serial('/dev/ttyACM0', 9600)

# MQTT Topics
control_topics = {
    'water_pump_control_topic': pump,
    'fan_control_topic': fan,
    'buzzer_control_topic': buzzer,
    'leds_control_topic': leds
}

def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with result code " + str(rc))
    for topic in control_topics.keys():
        client.subscribe(topic)

def on_publish(client, userdata, mid, properties=None):
    print("Message published with mid: " + str(mid))

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def control_device(device, value):
    if value == 1:
        device.on()
    else:
        device.off()

def on_message(client, userdata, msg):
    payload_str = msg.payload.decode().strip()

    try:
        payload_value = int(payload_str)
        print(f"Received integer message {payload_value} on topic '{msg.topic}' with QoS {msg.qos}")

        if msg.topic in control_topics:
            control_device(control_topics[msg.topic], payload_value)

        if msg.topic == 'leds_control_topic':
            for led in leds:
                control_device(led, payload_value)

    except ValueError:
        print(f"Failed to convert message '{payload_str}' to an integer.")

# Create an MQTT client instance
client = paho.Client()
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

# Enable TLS for secure connection
client.tls_set(tls_version=ssl.PROTOCOL_TLS)
client.username_pw_set("esraa2", "h4rgcBQbnMZ#8yY")
client.connect("0556f0e5afbb48d0b9308a4694834441.s1.eu.hivemq.cloud", 8883)

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            print(f"Received sensor data: {line}")

            data_parts = line.split(',')
            if len(data_parts) >= 2:
                sensor_name = data_parts[0].strip()
                sensor_value = float(data_parts[1].strip())

                topics = {
                    "Rain Level": "rain_sensor_topic",
                    "Flame": "flame_sensor_topic",
                    "Moisture Level": "soil_moisture_topic",
                    "Temperature": "temperature_humidity_topic",
                    "Humidity": "temperature_humidity_topic",
                    "LDR": "ldr_topic",
                    "Water Level": "water_level_topic"
                }
                
                if sensor_name in topics:
                    message = json.dumps({sensor_name.lower().replace(" ", "_"): sensor_value})
                    client.publish(topics[sensor_name], message)

                # Control logic for pump and buzzer based on sensor values
                if sensor_name == "Flame":
                    control_device(buzzer, 1 if sensor_value == 1 else 0)
                elif sensor_name == "Moisture Level":
                    control_device(pump, 1 if sensor_value < 70 else 0)

                # Control fan based on temperature and messages
                if sensor_name == "Temperature":
                    control_device(fan, 1 if sensor_value > 30 else 0)

                # Publish LED status based on LDR value
                led_active = any(sensor_value >= threshold for threshold in [10, 20, 30, 40, 50])
                for i, led in enumerate(leds):
                    control_device(led, 1 if sensor_value >= (i + 1) * 10 else 0)
                
                # Publish LED status based on activity
                client.publish("leds_topic", json.dumps({"leds": 1 if led_active else 0}))

except KeyboardInterrupt:
    print("Exiting...")

finally:
    ser.close()  # Close the serial connection
    client.loop_stop()  # Stop the MQTT loop
    pump.off()  # Ensure pump is off when exiting
    fan.off()   # Ensure fan is off when exiting
    buzzer.off()  # Ensure buzzer is off when exiting
    for led in leds:
        led.off()  # Ensure LEDs are off when exiting
