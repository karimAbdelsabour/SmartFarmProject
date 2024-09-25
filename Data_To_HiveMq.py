import time
import paho.mqtt.client as paho
import serial
import ssl  # Import the ssl module for TLS


# Set up the serial connection (adjust '/dev/ttyUSB0' to your setup)
ser = serial.Serial('/dev/ttyACM0', 9600)

# Setting callbacks for different events
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

def on_publish(client, userdata, mid, properties=None):
    print("Message published with mid: " + str(mid))

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

# Create an MQTT client instance
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

# Enable TLS for secure connection
client.tls_set(tls_version=ssl.PROTOCOL_TLS)  # Use the ssl module for TLS
# Set username and password
client.username_pw_set("karim", "France_2002")
# Connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect("285f8bca933f45b5aef1fdb699f6faea.s1.eu.hivemq.cloud", 8883)

# Subscribe to all topics of encyclopedia
client.subscribe("encyclopedia/#", qos=1)

# Publish data based on incoming serial data
try:
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
                    client.publish("water level", sensor_value)

                elif sensor_name == "Temperature":
                    client.publish("Temperature", sensor_value)

                elif sensor_name == "Humidity":
                    client.publish("Humidity", sensor_value)

                elif sensor_name == "SoilMoisture":
                    client.publish("Moisture", sensor_value)

                elif sensor_name == "Flame":
                    client.publish("flame", sensor_value)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    ser.close()  # Close the serial connection
    client.loop_stop()  # Stop the MQTT loop
