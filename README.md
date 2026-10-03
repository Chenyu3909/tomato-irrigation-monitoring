# Raspberry Pi Environmental Monitoring System

I built this Raspberry Pi monitoring system for a tomato irrigation experiment at the **Boyce Thompson Institute (BTI)** under the mentorship of **Yao Chen, Translational Scientist at BTI/Cornell**. The goal was to collect soil moisture, temperature, and humidity continuously in the field without relying on manual measurements.

I designed the hardware setup, integrated four analog soil-moisture sensors through an ADS1115 ADC, wrote the Python data logger, configured it to run automatically with `systemd`, and deployed the completed system outdoors. It logged measurements every **15 minutes for 37 days**, producing more than **34,000 individual sensor measurements**.

## Engineering Objective

I needed the system to:

- Read four analog soil-moisture sensors from a Raspberry Pi
- Measure ambient temperature and humidity
- Timestamp and save every reading
- Run without a laptop connected
- Recover from temporary DHT22 read errors instead of stopping
- Operate outdoors for several weeks
- Store the data for later analysis

## System Architecture

```text
                         ┌── DHT22
                         │   Temperature
                         │   Humidity
Raspberry Pi 4 ──────────┤
                         │
                         └── ADS1115 ADC
                                │
                                ├── Soil Sensor 1
                                ├── Soil Sensor 2
                                ├── Soil Sensor 3
                                └── Soil Sensor 4
```

The DHT22 connects directly to the Raspberry Pi. Because the Pi has no built-in analog inputs, I used an **ADS1115 16-bit ADC** to read the four capacitive soil-moisture sensors, one on each analog channel.

## Hardware Development

I built the system in stages rather than wiring everything at once. I started with the DHT22, then added the ADS1115 and tested the soil sensors before combining all four into the final setup.

![Raspberry Pi hardware build](images/01_hardware_build.jpeg)

*Raspberry Pi, breadboard, ADS1115, and sensor wiring during development.*

![Four-sensor bench test](images/02_four_sensor_bench_test.jpeg)

*Bench testing the complete four-sensor setup before field deployment.*

The outdoor enclosure is documented by the exported STL files [`cad/enclosure.stl`](cad/enclosure.stl) and [`cad/enclosure-lid.stl`](cad/enclosure-lid.stl).

## Software and Data Logging

The monitoring software is written in **Python** and is available here:

**[View the full sensor logger →](src/sensor_logger.py)**

The logger initializes the DHT22 and ADS1115, reads temperature, humidity, and all four soil-moisture sensors, timestamps each sampling cycle, and appends the readings to a CSV file. Each soil sensor is recorded as both a raw ADC value and voltage.

The sampling interval is set to 900 seconds (15 minutes):

```python
SAMPLE_INTERVAL_SECONDS = 900
```

I added error handling for temporary DHT22 read failures so a bad reading would not stop a long-term logging session. The required Python packages are listed in [`requirements.txt`](requirements.txt).

## Automated Operation

I configured the logger as a Linux `systemd` service, included at [`systemd/sensor_logger.service`](systemd/sensor_logger.service).

This let the Raspberry Pi run the monitoring program automatically instead of requiring me to manually start the script. During the original deployment, the service used `/home/chenyuyang` as its working directory and wrote readings to `environment_log.csv`.

## Field Deployment

After indoor testing, I installed the electronics in an enclosure and deployed the system with the tomato plants.

![Field deployment](images/03_field_deployment.jpeg)

*Monitoring system deployed in the planting area.*

![Enclosure interior](images/04_enclosure_interior.jpeg)

*Raspberry Pi and sensor electronics inside the outdoor enclosure.*

The system remained in the field for **37 days** while recording measurements every 15 minutes.

## Development Process

The main stages were:

1. Test temperature and humidity logging with the DHT22
2. Connect and configure the ADS1115 over I2C
3. Test individual capacitive soil-moisture sensors
4. Connect four sensors to separate ADC channels
5. Combine all sensor readings into one Python logger
6. Write timestamped readings to CSV
7. Set the logger to a 15-minute sampling interval
8. Configure automatic operation with `systemd`
9. Package the electronics for outdoor use
10. Deploy the completed system in the field

The earlier CSV files in `data/` preserve some of these development stages.

## Field Performance

The final logger produced [`data/environment_log.csv`](data/environment_log.csv). I also kept the earlier DHT-only and pre-deployment logs rather than deleting them.

### Temperature and Humidity

![Temperature and humidity over time](data/temperature-humidity-over-time.png)

### Soil Moisture

![Average soil moisture by irrigation treatment](data/soil-moisture-treatment-comparison.png)

The graphs are included here mainly to show the output of the monitoring system. The soil sensors report raw ADC readings rather than calibrated volumetric water content, so I kept the interpretation descriptive.

## Research Application

The engineering system supported a larger experiment asking:

> **How does soil moisture variability affect tomato fruit quality and blossom-end rot (BER)?**

The experiment included **20 tomato plants**, **5 cultivars**, and two irrigation treatments beginning July 3, 2026.

| Treatment | Irrigation schedule | Sensors |
| --- | --- | --- |
| Control | 10 minutes every day | Soil 3 & 4 |
| Experimental | 30 minutes every 3 days | Soil 1 & 2 |

The irrigation schedules were controlled separately from the Raspberry Pi. The system documented in this repository was used for **monitoring and data logging**, not irrigation control.

![Tomato experiment](images/05_tomato_experiment.jpeg)

*Monitoring system positioned in the experimental growing area.*

### BER Observation

![Tomato showing blossom-end rot](images/06_ber_observation.png)

*A fruit with visible blossom-end rot symptoms observed during the study.*

Fruit development was still ongoing during the documented study period, and BER observations were limited. I therefore did not use this observation to claim that either irrigation treatment caused or prevented BER.

The larger research project is summarized in the [**research poster (PDF)**](assets/poster/research-poster.pdf).

## Bill of Materials

Hardware and irrigation materials purchased for the project totaled **$280.77**. Project costs were funded by the **Boyce Thompson Institute (BTI)**.

| Component | Cost | Role |
| --- | ---: | --- |
| Raspberry Pi 4 | $134.99 | Data logging and storage |
| DHT22 | $13.99 | Temperature and humidity |
| ADS1115 | $7.99 | Analog-to-digital conversion |
| Soil Sensors #1 & #2 | $22.99 | Soil-moisture sensing |
| Soil Sensors #3 & #4 | $22.99 | Soil-moisture sensing |
| Breadboard and wires | $9.99 | Prototyping and wiring |
| Drip irrigation system | $26.99 | Experimental irrigation |
| Water timer | $40.84 | Irrigation timing |
| **Total** | **$280.77** | |

## Repository Structure

```text
tomato-irrigation-monitoring/
├── assets/poster/       # research poster
├── cad/                 # enclosure STL exports
├── data/                # field data, test data, and plots
├── images/              # build and deployment photos
├── src/                 # Python logger
├── systemd/             # automatic logger service
├── requirements.txt
└── README.md
```

## Running the Logger

Install the required libraries:

```bash
pip install -r requirements.txt
```

Run the logger:

```bash
python3 src/sensor_logger.py
```

The program creates or appends to `environment_log.csv` in its working directory. Hardware connections must match the GPIO and ADS1115 channel assignments in `sensor_logger.py`.

## Future Improvements

If I rebuilt the system, I would:

- Calibrate the soil sensors to estimate volumetric water content
- Improve weather protection for the electronics
- Add remote monitoring so I could check incoming data without physically accessing the Pi
- Add more sensors for greater spatial replication
- Integrate irrigation control with the Raspberry Pi

## Technologies

`Python` · `Raspberry Pi` · `Linux` · `systemd` · `I2C` · `ADS1115` · `DHT22` · `Analog Sensors` · `Data Logging`

## Acknowledgments

This system was developed for a tomato irrigation research project at the **Boyce Thompson Institute (BTI)** under the mentorship of **Yao Chen, Translational Scientist at BTI/Cornell**. Project hardware and materials were funded by BTI.
