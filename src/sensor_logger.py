import csv
import os
import time
from datetime import datetime

import adafruit_dht
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

LOG_FILE = "environment_log.csv"
SAMPLE_INTERVAL_SECONDS = 900

dht_device = adafruit_dht.DHT22(board.D4)

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

soil1 = AnalogIn(ads, 0)
soil2 = AnalogIn(ads, 1)
soil3 = AnalogIn(ads, 2)
soil4 = AnalogIn(ads, 3)


def ensure_csv_header():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "timestamp",
                "temperature_c",
                "humidity_percent",
                "soil1_value",
                "soil1_voltage",
                "soil2_value",
                "soil2_voltage",
                "soil3_value",
                "soil3_voltage",
                "soil4_value",
                "soil4_voltage"
            ])


def log_reading(row):
    with open(LOG_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(row)
        file.flush()


ensure_csv_header()

while True:
    try:
        timestamp = datetime.now().isoformat(timespec="seconds")

        temperature = dht_device.temperature
        humidity = dht_device.humidity

        row = [
            timestamp,
            temperature,
            humidity,
            soil1.value,
            round(soil1.voltage, 3),
            soil2.value,
            round(soil2.voltage, 3),
            soil3.value,
            round(soil3.voltage, 3),
            soil4.value,
            round(soil4.voltage, 3),
        ]

        log_reading(row)

        print(
            f"{timestamp} | Temp: {temperature} C | Humidity: {humidity}% | "
            f"Soil1: {soil1.value} | Soil2: {soil2.value} | "
            f"Soil3: {soil3.value} | Soil4: {soil4.value}"
        )

    except RuntimeError as error:
        print("Sensor read error:", error)
        time.sleep(2)
        continue

    except Exception as error:
        dht_device.exit()
        raise error

    time.sleep(SAMPLE_INTERVAL_SECONDS)
