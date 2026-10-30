# Pulse SyncAlert
### Pulse SyncAlert is a personalized, AI-powered, continuous cardiac monitoring prototype that uses machine learning to learn an individual's baseline heart rate, whether naturally elevated, naturally low, or population-level typical, and flags when an unusual pattern occurs. Most heart monitors compare you to population averages. Pulse SyncAlert compares you to yourself.

**Congressional App Challenge 2026 | FL-14**

## What It Does

Pulse SyncAlert is an end-to-end hardware-to-software prototype. The hardware is a MAX30102 pulse oximetry sensor and an Arduino Nano ESP32 microcontroller, with cables and jumper wires totaling $34.89 per unit. The sensor detects heart rate using infrared (IR) light, and the Arduino reads the sensor and sends each BPM/IR reading to the laptop over USB or built-in Wi-Fi. The AI core is an IsolationForest model from scikit-learn that can be trained on either Arduino output or synthetic heart rate data. Because it learns the pattern of the individual's data, it adapts to personal baselines and flags readings that are truly unusual for that specific person. Every reading receives a score: +1 for normal, -1 for a flagged anomaly. Results appear on a Streamlit dashboard with four pages: prototype information, a real-time dashboard, an AI anomaly log, and an education tab with information from the American Heart Association. Flagged readings are timestamped and downloadable so a patient can bring the report to a cardiologist appointment for a well-informed consultation.

*Pulse SyncAlert is not a medical device. It is a data awareness tool that flags heart rate anomalies and helps patients bring better information to their doctor.*

> **Note:** As real cardiac patient data carries significant privacy and HIPAA concerns, synthetic heart rate data that statistically replicates SVT episode patterns was generated, allowing the IsolationForest model to train without exposing any individual's health information. The synthetic database file is provided (synthetic_database.db).

## The Problem It Solves

Today's leading cardiac wearables fall short for millions of Americans in three ways:
- **No personalized baseline:** athletes with naturally low heart rates (30s-50s BPM) and hyperthyroid patients with naturally high heart rates get constant false alarms
- **Not truly continuous:** can miss SVT episodes that last only seconds
- **Cost:** commercial smartwatches at $400-$1,000 are not financially practical for many families, including the 92 million Americans who are uninsured or underinsured

The average cardiologist wait time in the US is 32.7 days. Pulse SyncAlert gives patients better information while they wait, with a downloadable timestamped report they can bring to their cardiologist appointment for a well-informed consultation.

## Hardware

**Cost per prototype (1 unit):**

| Component | Cost |
|-----------|------|
| Arduino Nano ESP32 | $19.30 |
| MAX30102 sensor | $2.66 |
| Jumper wires | $0.58 |
| USB-C cable | $9.85 |
| **Total** | **$34.89** |

The sensor detects heart rate using infrared (IR) light. The Arduino reads the sensor and sends each BPM/IR reading to the laptop over USB or built-in Wi-Fi.

## Hardware

**Cost per prototype (1 unit):**

| Component | Cost |
|-----------|------|
| Arduino Nano ESP32 | $19.30 |
| MAX30102 sensor | $2.66 |
| Jumper wires | $0.58 |
| USB-C cable | $9.85 |
| **Total** | **$34.89** |

The sensor detects heart rate using infrared (IR) light. The Arduino reads the sensor and sends each BPM/IR reading to the laptop over USB or built-in Wi-Fi.

## How the AI Works

**Synthetic Training Data:** Heart rate data is protected health information (HIPAA), so synthetic heart rate data that statistically replicates SVT episode patterns was generated using Python's `random.gauss()`, allowing the IsolationForest model to train without exposing any individual's health information.

Heart rate naturally clusters around a personal mean, so Gaussian distribution captures that well. Each parameter in the function maps to a real medical concept: resting rate, SVT rate, episode frequency, episode length, and spread. 10,000 heart rate readings from one function call. Parameters: normal baseline at 85 BPM, SVT episodes at 170+ BPM.

The synthetic database file is provided (synthetic_database.db).

**IsolationForest (scikit-learn):** Normal readings cluster together. Anomalies stand alone and are cut off in just a few splits. Outliers are easy to isolate; inliers are harder. Fewer cuts means more anomalous. That is how the model flags SVT. Output: `+1` (normal) or `-1` (anomaly).

**Real-time pipeline:** Each BPM reading (Arduino or synthetic data) → IsolationForest score → SQLite log → Streamlit dashboard update.

## App Pages
| Tab | Description |
|-----|-------------|
| Prototype Info | Hardware specs, coding language, backend tools used to build it, IsolationForest AI model training, and dashboard and other developmental tools used |
| Dashboard | BPM streaming in from the Arduino or synthetic data. Live BPM chart with red dots marking flagged anomalies, and a downloadable report to bring to a doctor appointment |
| Anomaly Log | Every flagged reading, timestamped, with BPM and deviation from baseline — ready to bring to a cardiologist |
| Education | What is SVT, symptoms to watch for, when to see a doctor or call 911 |


## Tech Stack
- **Python** — data generation, ML pipeline, serial communication
- **scikit-learn** — IsolationForest anomaly detection
- **SQLite** — local real-time database
- **Streamlit** — four-page web dashboard
- **Arduino (C++)** — sensor serial communication

## How to Run
The live app is deployed at the link below — no installation needed.

To run locally:
```bash
pip install streamlit scikit-learn pandas pyserial
streamlit run Dashboard.py
```

**Data flow:** Arduino serial readings or synthetic data are ingested in real time → written directly to a local SQLite database → IsolationForest scores each reading (`+1` normal or `-1` anomaly) → dashboard updates automatically.

> **Note to users:** The synthetic database is pre-loaded so the app runs fully without hardware. The dashboard, anomaly log, and flagged readings are all visible at the live link below without any setup.

## Live App
[pulsesyncalert.streamlit.app](https://pulsesyncalert.streamlit.app)

## Important Note
Pulse SyncAlert is a prototype and educational tool. It does not diagnose
or treat any medical condition. It flags deviations from a personal baseline
and helps patients bring better information to their cardiologist.

## Congressional App Challenge
Submitted to Congressional App Challenge 2026, FL-14.  
All code written by Angela Chen.
