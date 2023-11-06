# Demo of an unsecured API server under attack
For CZ4062 Computer Security (Group 63)

## Architecture
- Data: CSV file containing fake user data
- Backend: Flask API server
- Attack script: Python script

## Setup
Install requirements
> pip install requirements.txt

## Usage
1. Start flask API server
    - automatically loads and parses _user_data.csv_ as its "database"
    > python server.py

2. Run attack script in a separate terminal instance
    - stolen data is output as _stolen_data.csv_
    > python steal.py