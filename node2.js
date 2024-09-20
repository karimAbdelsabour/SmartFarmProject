const express = require('express');
const http = require('http');
const mqtt = require('mqtt');
const socketIO = require('socket.io');
const fs = require('fs');
const path = require('path');

// Set up the Express server
const app = express();
const server = http.createServer(app);

// Path to the log file
const logFilePath = path.join(__dirname, 'mqtt_logs.txt');

// Function to log messages to a file
const logToFile = (message) => {
    fs.appendFile(logFilePath, `${new Date().toISOString()} - ${message}\n`, (err) => {
        if (err) {
            console.error('Error writing to log file:', err);
        }
    });
};

// MQTT connection options
const mqttOptions = {
    host: '0556f0e5afbb48d0b9308a4694834441.s1.eu.hivemq.cloud',
    port: 8883,
    protocol: 'mqtts',
    username: 'esraa2',
    password: 'h4rgcBQbnMZ#8yY'
};

// Connect to the HiveMQ MQTT broker
const client = mqtt.connect(mqttOptions);

// Set up Socket.io on the server
const io = socketIO(server);

client.on('connect', () => {
    const message = 'Connected to HiveMQ MQTT broker';
    console.log(message);
    logToFile(message);

    // Subscribe to the topics you need
    const topics = [
        'temperature_humidity_topic',
        'soil_moisture_topic',
        'water_pump_topic',
        'motor_topic',
        'rain_sensor_topic',
        'flame_sensor_topic',
        'leds_topic',
        'water_level_topic',
        'ldr_topic',
        'leds_control_topic',
        'water_pump_control_topic',
        'fan_control_topic',
        'buzzer_control_topic'
    ];

    client.subscribe(topics, (err) => {
        if (err) {
            const errorMessage = `Error subscribing to topics: ${err}`;
            console.error(errorMessage);
            logToFile(errorMessage);
        } else {
            const successMessage = `Subscribed to topics: ${topics}`;
            console.log(successMessage);
            logToFile(successMessage);
        }
    });
});

// Handle incoming MQTT messages and send them to the front-end
client.on('message', (topic, message) => {
    const logMessage = `Received message from ${topic}: ${message.toString()}`;
    console.log(logMessage);
    logToFile(logMessage);

    // Emit the message to the front-end using Socket.io
    io.emit('mqtt_message', { topic, payload: message.toString() });
});

// Handle control commands
app.use(express.json());

app.post('/api/control', (req, res) => {
    const { topic, value } = req.body;
    if (topic && value) {
        client.publish(topic, value, (err) => {
            if (err) {
                console.error(`Error publishing to ${topic}:`, err);
                res.status(500).send('Error publishing control command');
            } else {
                console.log(`Published to ${topic}: ${value}`);
                res.send('Control command sent');
            }
        });
    } else {
        res.status(400).send('Invalid control command');
    }
});

// Serve static files (your front-end HTML, CSS, JS)
app.use(express.static(path.join(__dirname, 'public')));

// Start the Express server
const PORT = 3000;
server.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
