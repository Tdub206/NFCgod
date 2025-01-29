#!/bin/bash

echo "Installing dependencies..."
sudo apt update && sudo apt install -y python3 python3-pip nodejs npm openjdk-11-jdk
pip3 install -r requirements.txt

echo "Setting up frontend..."
cd frontend
npm install
npm run build
cd ..

echo "Setup complete. Run the backend with 'python3 backend/sniff_all.py'."
