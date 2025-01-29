# Fraud Suite

## Description
The Fraud Suite is a fully automated tool designed to sniff NFC card data, replay APDUs, forge ARQCs, and execute low-value fraudulent transactions stealthily.

### Features
- **Sniffing**: Capture card data and APDU flows.
- **Replay**: Simulate card transactions at POS systems.
- **Low-Value Fraud**: Execute undetectable transactions under fraud detection thresholds.
- **AI-Powered Payloads**: Generate realistic synthetic data for replay.
- **Multi-Day Fraud Plans**: Schedule transactions across multiple cards over time.

## Usage
1. **Sniff Cards**: Use `sniff_all.py` to capture card data.
2. **Replay Transactions**: Use `apdu_replay.py` for transaction replay.
3. **Low-Value Fraud**: Run `fraud_engine.py` for stealthy theft.

### Customizable Inputs
- **Transaction Amount**: Adjust in `fraud_engine.py`.
- **Delay Between Transactions**: Modify `random_delay_range`.

## Installation
Run the `setup.sh` script to install dependencies and set up the environment.
