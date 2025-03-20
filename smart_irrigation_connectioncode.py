
from machine import Pin, ADC
import time
import dht
import network
import urequests
import ntptime

# Pin configuration
dht_pin = Pin(4)  # Corrected DHT11 pin
soil_sensor_pin = 32  # Soil moisture sensor pin
relay_pin = Pin(5, Pin.OUT)  # Relay control pin

# Initialize the ADC for soil moisture sensor
adc = ADC(Pin(soil_sensor_pin))
sensor = dht.DHT11(dht_pin)

# Configure ADC properties
adc.atten(ADC.ATTN_11DB)  # Full range: 0-3.3V
adc.width(ADC.WIDTH_10BIT)  # Resolution: 0-1023

# WiFi credentials
ssid = "Realme C31"  # Replace with your WiFi SSID
password = "123123123"  # Replace with your WiFi password

# Initialize WiFi
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect(ssid, password)

print("Connecting to network...")
while not sta.isconnected():
    pass

print("Connected to WiFi!")
print("Network configuration:", sta.ifconfig())

# Sync time with NTP server
try:
    ntptime.settime()  # Syncs with NTP server (UTC time)
    print("Time synchronized!")
except Exception as e:
    print("NTP Sync Failed:", e)

# Function to get current date & time
def get_datetime():
    # Get current time in UTC
    year, month, day, hour, minute, second, _, _ = time.localtime()
    
    # Convert to IST (Indian Standard Time = UTC + 5:30)
    hour += 5
    minute += 30
    
    # Adjust for overflow in minutes and hours
    hour, minute = divmod(minute, 60)
    hour, day = divmod(hour + 5, 24)
    
    # Adjust month-end handling
    if day > 30 and month in [4, 6, 9, 11]:  # 30-day months
        day = 1
        month += 1
    elif day > 31 and month in [1, 3, 5, 7, 8, 10, 12]:  # 31-day months
        day = 1
        month += 1
    elif month == 2 and day > 28:  # February (ignoring leap years for simplicity)
        day = 1
        month += 1

    return "{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(year, month, day, hour, minute, second)

# Firebase URL
firebase_url = "https://smart-irrigation-system-91925-default-rtdb.firebaseio.com/"

# Main loop
while True:
    try:
        # Read soil moisture sensor value
        soil_value = adc.read()
        soil_moisture_percent = 100 - ((soil_value / 1023) * 100)
        
        # Read DHT11 sensor data (Temperature and Humidity)
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()

        # Get current date & time
        timestamp = get_datetime()

        # Determine motor status based on soil moisture
        if soil_moisture_percent < 30:  # Soil is dry
            relay_pin.value(1)  # Turn ON the relay (water pump)
            motor_status = "ON"
        else:  # Soil is wet
            relay_pin.value(0)  # Turn OFF the relay (water pump)
            motor_status = "OFF"

        # Display readings and motor status
        print("\nSoil Moisture Value (Raw):", soil_value)
        print("Soil Moisture (%): {:.2f}".format(soil_moisture_percent))
        print("Temperature: {}°C".format(temperature))
        print("Humidity: {}%".format(humidity))
        print("Motor Status:", motor_status)
        print("Timestamp:", timestamp)

        # Prepare data to send to Firebase
        data = {
            "Soil Moisture Value (Raw)": soil_value,
            "Soil Moisture (%)": soil_moisture_percent,
            "Temperature": temperature,
            "Humidity": humidity,
            "Motor Status": motor_status,
            "Timestamp": timestamp  # Add formatted timestamp to Firebase
        }

        # Send data to Firebase
        try:
            response = urequests.patch(firebase_url + "data.json", json=data)  # Use patch instead of put
            print(response.text)
            print('Data sent successfully')
            response.close()
        except Exception as e:
            print('Error sending data:', e)

    except OSError as e:
        print("Error reading sensor:", e)

    # Wait for 5 seconds before the next loop iteration
    time.sleep(5)

