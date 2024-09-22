import paho.mqtt.client as mqtt
import json
import serial  # Import serial library for reading data
import time

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def on_publish(client, userdata, mid):
    print("Message published")

# Set up the serial connection (adjust '/dev/ttyUSB0' to your setup)
ser = serial.Serial('/dev/ttyACM0', 9600)

# Create nine separate MQTT clients
client_water_level = mqtt.Client()
client_temp_humidity = mqtt.Client()
client_soil_moisture = mqtt.Client()
client_ldr = mqtt.Client()
client_water_pump = mqtt.Client()
client_motor = mqtt.Client()
client_rain_sensor = mqtt.Client()
client_flame_sensor = mqtt.Client()
client_leds = mqtt.Client()

client_water_level.on_connect = on_connect
client_water_level.on_publish = on_publish

client_temp_humidity.on_connect = on_connect
client_temp_humidity.on_publish = on_publish

client_soil_moisture.on_connect = on_connect
client_soil_moisture.on_publish = on_publish

client_ldr.on_connect = on_connect
client_ldr.on_publish = on_publish

client_water_pump.on_connect = on_connect
client_water_pump.on_publish = on_publish

client_motor.on_connect = on_connect
client_motor.on_publish = on_publish

client_rain_sensor.on_connect = on_connect
client_rain_sensor.on_publish = on_publish

client_flame_sensor.on_connect = on_connect
client_flame_sensor.on_publish = on_publish

client_leds.on_connect = on_connect
client_leds.on_publish = on_publish

# Set up the ThingsBoard MQTT server address and port
broker = "mqtt.thingsboard.cloud"
port = 1883

# Define topics for different devices
water_level_topic = "v1/devices/me/telemetry"
temperature_humidity_topic = "v1/devices/me/telemetry"
soil_moisture_topic = "v1/devices/me/telemetry"
ldr_topic = "v1/devices/me/telemetry"
water_pump_topic = "v1/devices/me/telemetry"
motor_topic = "v1/devices/me/telemetry"
rain_sensor_topic = "v1/devices/me/telemetry"
flame_sensor_topic = "v1/devices/me/telemetry"
leds_topic = "v1/devices/me/telemetry"

# Define device tokens for each device
water_level_token = "f86990dj9jcrmqwi67z1"
temp_humidity_token = "43btkYGvLA7p8n80glCW"
soil_moisture_token = "lLUSkMbUVxmsVYkL2lz6"
ldr_token = "UkgyNoAVthsT2nzQ3SYl"
water_pump_token = "WGQdpkbIdYdB7WoWG5Ya"
motor_token = "4wL9gHIdNOcbjCkfnKPq"
rain_sensor_token = "k5uPxduByhOVRNzW6yHN"
flame_sensor_token = "C6EmnQNZAIWEkSOe6XOf"
leds_token = "HnETpSubTdveTlqC4jL9"

# Connect and authenticate for all devices
def connect_client(client, token):
    client.username_pw_set(token, "")
    client.connect(broker, port, 60)

connect_client(client_water_level, water_level_token)
connect_client(client_temp_humidity, temp_humidity_token)
connect_client(client_soil_moisture, soil_moisture_token)
connect_client(client_ldr, ldr_token)
connect_client(client_water_pump, water_pump_token)
connect_client(client_motor, motor_token)
connect_client(client_rain_sensor, rain_sensor_token)
connect_client(client_flame_sensor, flame_sensor_token)
connect_client(client_leds, leds_token)

client_water_level.loop_start()
client_temp_humidity.loop_start()
client_soil_moisture.loop_start()
client_ldr.loop_start()
client_water_pump.loop_start()
client_motor.loop_start()
client_rain_sensor.loop_start()
client_flame_sensor.loop_start()
client_leds.loop_start()

# Publish data based on incoming serial data
while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()  # Read a line from the serial
        print(f"Received: {line}")  # Print the received data

        # Parse the incoming data
        data_parts = line.split(',')
        if len(data_parts) >= 2:
            sensor_name = data_parts[0]
            sensor_value = data_parts[1]

            # Publish based on the sensor name
            if sensor_name == "WaterLevel":
                water_level_data = {"water_level": float(sensor_value)}
                client_water_level.publish(water_level_topic, json.dumps(water_level_data))

            elif sensor_name == "Temperature":
                temp_humidity_data = {"temperature": float(sensor_value)}
                client_temp_humidity.publish(temperature_humidity_topic, json.dumps(temp_humidity_data))

            elif sensor_name == "Humidity":
                temp_humidity_data = {"humidity": float(sensor_value)}
                client_temp_humidity.publish(temperature_humidity_topic, json.dumps(temp_humidity_data))

            elif sensor_name == "SoilMoisture":
                soil_moisture_data = {"soil_moisture": float(sensor_value)}
                client_soil_moisture.publish(soil_moisture_topic, json.dumps(soil_moisture_data))

            elif sensor_name == "Flame":
                flame_sensor_data = {"flame_sensor": bool(int(sensor_value))}
                client_flame_sensor.publish(flame_sensor_topic, json.dumps(flame_sensor_data))

            # Add more sensor cases as needed

    time.sleep(1)  # Adjust delay as necessary

client.loop_stop()
client.disconnect()
