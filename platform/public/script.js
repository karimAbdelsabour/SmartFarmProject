const socket = io();

//to get data from nodeJS
socket.on('mqtt_message', (data) => {
    console.log(`Received message from ${data.topic}: ${data.payload}`);
    try {
        const payload = JSON.parse(data.payload);
        updateStatus(payload);
    } catch (error) {
        console.error('Error parsing MQTT payload:', error);
    }
});

function updateIcon(element, iconClass) {
    element.className = ''; 
    element.classList.add('fas', iconClass); 
}

function updateAlertClass(alertElement, addClass, removeClass) {
    alertElement.classList.remove(removeClass);
    alertElement.classList.add(addClass);
}

//update status of the container including the color, icon and text
function updateStatus(payload) {
    if (payload.temperature !== undefined) {
        const temperature = parseFloat(payload.temperature);
        const tempElement = document.getElementById('temperature-status');
        const tempIcon = document.getElementById('temperature-icon');
        const tempAlert = document.getElementById('temperature-alert');
        tempElement.innerText = `${temperature} °C`;

        if (temperature < 20) {
            updateAlertClass(tempAlert, 'alert-low-temp', 'alert-high-temp');
            updateAlertClass(tempAlert, 'alert-low-temp', 'alert-medium-temp');
            updateIcon(tempIcon, 'fa-thermometer-quarter');
            tempElement.innerText = `Low Temperature: ${temperature} °C`;
        } else if (temperature >= 20 && temperature < 30) {
            updateAlertClass(tempAlert, 'alert-medium-temp', 'alert-low-temp');
            updateAlertClass(tempAlert, 'alert-medium-temp', 'alert-high-temp');
            updateIcon(tempIcon, 'fa-thermometer-half');
            tempElement.innerText = `Medium Temperature: ${temperature} °C`;
        } else {
            updateAlertClass(tempAlert, 'alert-high-temp', 'alert-low-temp');
            updateAlertClass(tempAlert, 'alert-high-temp', 'alert-medium-temp');
            updateIcon(tempIcon, 'fa-thermometer-full');
            tempElement.innerText = `High Temperature: ${temperature} °C`;
        }
    }

    if (payload.rain_sensor !== undefined) {
        const rainElement = document.getElementById('rain-detection-status');
        const rainIcon = document.getElementById('rain-icon');
        const rainAlert = document.getElementById('rain-alert');
        if (payload.rain_sensor == '1') {
            rainElement.innerText = 'Detected';
            updateAlertClass(rainAlert, 'alert-rain', 'alert-no-rain');
            updateIcon(rainIcon, 'fa-cloud-showers-heavy'); 
        } else {
            rainElement.innerText = 'Not Detected';
            updateAlertClass(rainAlert, 'alert-no-rain', 'alert-rain');
            updateIcon(rainIcon, 'fa-cloud');  
        }
    }


    if (payload.ldr !== undefined) {
        const ldrElement = document.getElementById('ldr-status');
        const ldrIcon = document.getElementById('ldr-icon');
        const ldrAlert = document.getElementById('ldr-alert');
        if (payload.ldr == '1') {
            ldrElement.innerText = 'Light';
            updateAlertClass(ldrAlert, 'alert-light', 'alert-dark');
            updateIcon(ldrIcon, 'fa-sun');  
        } else {
            ldrElement.innerText = 'Dark';
            updateAlertClass(ldrAlert, 'alert-dark', 'alert-light');
            updateIcon(ldrIcon, 'fa-moon');  
        }
    }

    if (payload.flame_sensor !== undefined) {
        const fireElement = document.getElementById('fire-warning-status');
        const fireIcon = document.getElementById('fire-icon');
        const fireAlert = document.getElementById('fire-alert');
        if (payload.flame_sensor == '1') {
            fireElement.innerText = 'Warning';
            updateAlertClass(fireAlert, 'alert-fire-warning', 'alert-fire-safe');
            updateIcon(fireIcon, 'fa-exclamation-triangle');  
        } else {
            fireElement.innerText = 'Safe';
            updateAlertClass(fireAlert, 'alert-fire-safe', 'alert-fire-warning');
            updateIcon(fireIcon, 'fa-check'); 
        }
    }
}


function updateStatusDisplay(topic, status) {
    if (topic === 'leds_control_topic') {
        document.getElementById('leds-status').innerText = status;
        const ledsState = document.getElementById('leds-status');
        ledsState.classList.toggle('inactive', status === 'Inactive');
        updateButtonState('leds-toggle', status);
    }
    
}



function sendControlCommand(topic, value) {
    fetch('/api/control', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ topic, value })
    })
    .then(response => response.text())
    .then(data => {
        console.log('Command sent:', data);
        const status = value === '1' ? 'Active' : 'Inactive';
        updateStatusDisplay(topic, status);
    })
    .catch(error => console.error('Error:', error));
}

// Update the display status based on topic
function updateStatusDisplay(topic, status) {
    if (topic === 'leds_control_topic') {
        document.getElementById('leds-status').innerText = status;
        const ledsState = document.getElementById('leds-status');
        ledsState.classList.toggle('inactive', status === 'Inactive');
        updateButtonState('leds-toggle', status);
    } else if (topic === 'water_pump_control_topic') {
        document.getElementById('water-pump-status').innerText = status;
        const pumpState = document.getElementById('water-pump-status');
        pumpState.classList.toggle('inactive', status === 'Inactive');
        updateButtonState('water-pump-toggle', status);
    } else if (topic === 'fan_control_topic') {
        document.getElementById('fan-status').innerText = status;
        const fanState = document.getElementById('fan-status');
        fanState.classList.toggle('inactive', status === 'Inactive');
        updateButtonState('fan-toggle', status);
    } else if (topic === 'buzzer_control_topic') {
        document.getElementById('buzzer-status').innerText = status;
        const buzzerState = document.getElementById('buzzer-status');
        buzzerState.classList.toggle('inactive', status === 'Inactive');
        updateButtonState('buzzer-toggle', status);
    }
}

// Update button text based on status
function updateButtonState(buttonId, status) {
    const button = document.getElementById(buttonId);
    if (status === 'Active') {
        button.innerText = `Turn Off ${buttonId.split('-')[0].charAt(0).toUpperCase() + buttonId.split('-')[0].slice(1)}`;
        button.classList.remove('inactive');
    } else {
        button.innerText = `Turn On ${buttonId.split('-')[0].charAt(0).toUpperCase() + buttonId.split('-')[0].slice(1)}`;
        button.classList.add('inactive');
    }
}

// Event listeners for control buttons
document.getElementById('buzzer-toggle').addEventListener('click', () => {
    const currentStatus = document.getElementById('buzzer-status').innerText === 'Active' ? '0' : '1';
    sendControlCommand('buzzer_control_topic', currentStatus);
});
document.getElementById('water-pump-toggle').addEventListener('click', () => {
    const currentStatus = document.getElementById('water-pump-status').innerText === 'Active' ? '0' : '1';
    sendControlCommand('water_pump_control_topic', currentStatus);
});
document.getElementById('fan-toggle').addEventListener('click', () => {
    const currentStatus = document.getElementById('fan-status').innerText === 'Active' ? '0' : '1';
    sendControlCommand('fan_control_topic', currentStatus);
});
document.getElementById('leds-toggle').addEventListener('click', () => {
    const currentStatus = document.getElementById('leds-status').innerText === 'Active' ? '0' : '1';
    sendControlCommand('leds_control_topic', currentStatus);
});

// Navbar functionality
const hamburger = document.querySelector(".hamburger");
const navMenu = document.querySelector(".nav-menu");

hamburger.addEventListener("click", mobileMenu);

function mobileMenu() {
    hamburger.classList.toggle("active");
    navMenu.classList.toggle("active");
}






