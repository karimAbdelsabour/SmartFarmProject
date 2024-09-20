import paho.mqtt.client as mqtt
import json
import random
import time

# Function to generate random sensor data
def generate_sensor_data():
    return {
        "temperature": round(random.uniform(15.0, 30.0), 2),
        "humidity": round(random.uniform(30.0, 70.0), 2),
        "soil_moisture": round(random.uniform(10.0, 100.0), 2),
        "ldr": round(random.uniform(0.0, 100.0), 2),
        "water_pump": random.randint(0, 1),
        "motor": random.randint(0, 1),
        "rain_sensor": random.randint(0, 1),
        "flame_sensor": random.randint(0, 1),
        "leds": random.randint(0, 1),
        "water_level": round(random.uniform(0.0, 100.0), 2)
    }

# MQTT connection and publishing
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
    else:
        print(f"Connection failed with code {rc}")

client = mqtt.Client()
client.on_connect = on_connect

# Set up TLS connection
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
client.username_pw_set("esraa2", "h4rgcBQbnMZ#8yY")
client.connect("0556f0e5afbb48d0b9308a4694834441.s1.eu.hivemq.cloud", 8883, 60)

client.loop_start()

# Publishing sensor data
try:
    while True:
        data = generate_sensor_data()  # Generate new data each loop
        
        # Publish temperature and humidity
        temp_humidity_payload = json.dumps({
            "temperature": data["temperature"],
            "humidity": data["humidity"]
        })
        client.publish("temperature_humidity_topic", temp_humidity_payload)
        print(f"Published to temperature_humidity_topic: {temp_humidity_payload}")
        
        # Publish other sensor data
        for sensor in ["soil_moisture", "ldr", "water_pump", "motor", "rain_sensor", "flame_sensor", "leds", "water_level"]:
            payload = json.dumps({sensor: data[sensor]})
            client.publish(f"{sensor}_topic", payload)
            print(f"Published to {sensor}_topic: {payload}")

        time.sleep(5)  # Publish every 5 seconds
except KeyboardInterrupt:
    print("Publishing stopped")
finally:
    client.loop_stop()
    client.disconnect()
