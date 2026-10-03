# Raspberry Pi Tomato Irrigation Monitoring System

I built this Raspberry Pi monitoring system for a tomato irrigation experiment at the **Boyce Thompson Institute (BTI)**. The goal was to collect temperature, humidity, and soil-moisture data continuously in the field so I could compare conditions under two irrigation schedules and study their relationship with blossom-end rot (BER).

The final system used a Raspberry Pi 4, DHT22, ADS1115, and four capacitive soil-moisture sensors. A Python logger recorded all six sensor channels every 15 minutes and ran automatically with `systemd`.

## System

- **Raspberry Pi 4** — data logging and storage
- **DHT22** — ambient temperature and relative humidity
- **ADS1115** — analog-to-digital conversion for the soil sensors
- **4 capacitive soil-moisture sensors** — two sensors per irrigation treatment
- **Python + systemd** — automatic 15-minute logging

```text
                         ┌── DHT22
                         │   Temperature
                         │   Humidity
Raspberry Pi 4 ──────────┤
                         │
                         └── ADS1115
                              ├── Soil 1 ── Experimental
                              ├── Soil 2 ── Experimental
                              ├── Soil 3 ── Control
                              └── Soil 4 ── Control
```

The deployed logger is in [`src/sensor_logger.py`](src/sensor_logger.py). It saves a timestamp, temperature, humidity, and the raw value and voltage from each soil sensor. The sampling interval is set to 900 seconds (15 minutes).

## Building and Testing

I built the system in stages, starting with the DHT22 before adding the ADS1115 and four soil sensors. I tested the sensors in soil before combining everything into the final logger and configuring it to start automatically.

![Hardware build](images/01_hardware_build.jpeg)

*Early hardware integration with the Raspberry Pi, ADS1115, and sensors.*

![Four-sensor bench test](images/02_four_sensor_bench_test.jpeg)

*Testing all four soil-moisture sensors before field deployment.*

The enclosure parts used for the outdoor setup are included as STL files in the [`cad/`](cad/) folder.

## Field Deployment

After bench testing, I deployed the system outdoors with the tomato plants. The electronics were placed inside an enclosure, while the soil sensors were positioned in the experimental growing area.

![Field deployment](images/03_field_deployment.jpeg)

*The monitoring system deployed in the planting area.*

![Enclosure interior](images/04_enclosure_interior.jpeg)

*Raspberry Pi and sensor electronics inside the outdoor enclosure.*

## Experiment

The research question was:

> **How does soil moisture variability affect tomato fruit quality and blossom-end rot (BER)?**

The experiment included **20 tomato plants**, **5 cultivars**, and **2 irrigation treatments**. Irrigation treatments began July 3, 2026.

| Treatment | Irrigation schedule | Sensors |
| --- | --- | --- |
| Control | 10 minutes every day | Soil 3 & 4 |
| Experimental | 30 minutes every 3 days | Soil 1 & 2 |

The irrigation schedules were controlled separately from the Raspberry Pi. The Raspberry Pi system documented here was used for environmental monitoring and data logging, not irrigation control.

![Tomato experiment](images/05_tomato_experiment.jpeg)

*Monitoring system positioned in the outdoor experimental area.*

## Data and Results

The field logger ran for **37 days** at 15-minute intervals and produced more than **34,000 individual sensor measurements** across temperature, humidity, and four soil-moisture channels.

The final dataset is in [`data/environment_log.csv`](data/environment_log.csv). I also kept the earlier DHT-only and pre-deployment logs to document the development process.

### Temperature and Humidity

![Temperature and humidity over time](data/temperature-humidity-over-time.png)

### Soil Moisture

![Average soil moisture by treatment](data/soil-moisture-treatment-comparison.png)

The two treatment averages followed broadly similar patterns during the plotted period. Since the sensors report raw readings rather than calibrated volumetric water content, I kept the analysis descriptive rather than treating the values as absolute soil-moisture percentages.

### BER Observation

![Tomato showing blossom-end rot](images/06_ber_observation.png)

*A fruit with visible blossom-end rot symptoms observed during the study.*

Fruit development was still ongoing during the documented study period, and BER observations were limited. I therefore did not use these observations to claim that either irrigation treatment caused or prevented BER.

The research poster is available here: [**Research Poster (PDF)**](assets/poster/research-poster.pdf).

## Cost

Hardware and irrigation materials purchased for the project totaled **$280.77**. **Project costs were funded by the Boyce Thompson Institute (BTI).**

| Item | Cost | Purpose |
| --- | ---: | --- |
| Raspberry Pi 4 | $134.99 | Data logger |
| DHT22 | $13.99 | Temperature/humidity |
| ADS1115 | $7.99 | Analog conversion |
| Soil Sensors #1 & #2 | $22.99 | Soil-moisture sensing |
| Soil Sensors #3 & #4 | $22.99 | Soil-moisture sensing |
| Breadboard and wires | $9.99 | Prototyping and wiring |
| Drip irrigation system | $26.99 | Irrigation |
| Water timer | $40.84 | Irrigation timing |
| **Total** | **$280.77** | |

## Repository

```text
tomato-irrigation-monitoring/
├── assets/poster/       # research poster
├── cad/                 # enclosure STL files
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

Then run:

```bash
python3 src/sensor_logger.py
```

The program creates or appends to `environment_log.csv` in its working directory. Hardware connections must match the GPIO and ADS1115 channel assignments in the logger.

## What I Would Improve

If I continued the system, I would calibrate the soil sensors to estimate volumetric water content, add more sensor replication, improve weather protection, and add remote data visualization. I would also explore integrating irrigation control so the monitoring and treatment systems could operate from the same platform.

## Technologies

`Python` · `Raspberry Pi` · `Linux` · `systemd` · `I2C` · `ADS1115` · `DHT22` · `Environmental Sensing` · `Data Logging`

## Acknowledgments

This project was completed as part of tomato research at the **Boyce Thompson Institute**. Hardware and experimental material costs were funded by BTI.
