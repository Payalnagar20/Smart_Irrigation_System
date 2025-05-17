import requests
import time
import csv
import os
import json

# Firebase Realtime Database URL
firebase_url = "https://smart-irrigation-system-91925-default-rtdb.firebaseio.com/data.json"

# CSV file name
csv_filename = "IrrigationData_ReportStyle.csv"

# Create file if it doesn't exist
def ensure_csv_file():
    if not os.path.exists(csv_filename):
        with open(csv_filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Sensor Data Report"])
        print(f"✅ CSV file '{csv_filename}' created.")

# Fetch data from Firebase
def fetch_data():
    try:
        response = requests.get(firebase_url)
        if response.status_code == 200:
            return response.json()
        else:
            print("❌ Error fetching data:", response.status_code)
    except Exception as e:
        print("❌ Exception during fetch:", e)
    return None

# Run logging loop
last_timestamp = None
ensure_csv_file()

while True:
    data = fetch_data()
    if data:
        timestamp = data.get("Timestamp")
        if timestamp and timestamp != last_timestamp:
            # Prepare a single string report
            report = f"""Soil Moisture Value (Raw): {data.get('Soil Moisture Value (Raw)')}
Soil Moisture (%): {round(data.get('Soil Moisture (%)', 0), 2)}
Temperature: {data.get('Temperature')}°C
Humidity: {data.get('Humidity')}%
Motor Status: {data.get('Motor Status')}
Timestamp: {timestamp}
{json.dumps(data)}
Data sent successfully"""

            try:
                with open(csv_filename, mode="a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([report])
                last_timestamp = timestamp
                print(f"✅ Logged detailed data at {timestamp}")
            except Exception as e:
                print("❌ Error writing to CSV:", e)
        else:
            print("⏳ No new data or timestamp unchanged.")
    else:
        print("⚠️ Failed to fetch data from Firebase.")

    time.sleep(5)
