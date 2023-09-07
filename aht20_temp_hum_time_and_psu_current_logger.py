# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 11:20:28 2023

@author: matas.kirstukas
"""

import serial
import subprocess
import re
import pandas as pd
from datetime import datetime
from tenma import Tenma72_2535

# process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
# output, _ = process.communicate()

# Configure the serial port
ser = serial.Serial('COM5', baudrate=115200, timeout=1) # sensor
psu = Tenma72_2535('COM16') # psu

# Initialize an empty data frame
data_frame = pd.DataFrame(columns=["Timestamp", "Temperature", "Humidity", "PSU current"])

#%%

psu.setVoltage(1, 16800)    # set PSU voltage in mV
psu.setCurrent(1, 500)    # set PSU current in mA
psu.ON()                   # turn on PSU

try:
    while True:
        # Read temperature data
        temperature_line = ser.readline().decode('utf-8').strip()
        
        # Read humidity data
        humidity_line = ser.readline().decode('utf-8').strip()
        
        # Read current data
        psu_current = float(psu.runningCurrent(1))
        
        # Assuming the data format is "Temperature: XX.XX" and "Humidity: XX.XX"
        if temperature_line.startswith("Temperature:") and humidity_line.startswith("Humidity:"):
            temperature_data = temperature_line.split(" ")
            humidity_data = humidity_line.split(" ")
            
            temperature = float(temperature_data[1])
            humidity = float(humidity_data[1])
            
             
            # Get the current timestamp in the desired format
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            # Create a new DataFrame with the current data
            new_data = pd.DataFrame({"Timestamp": [timestamp],
                                      "Temperature": [temperature],
                                      "Humidity": [humidity],
                                      "PSU current": [psu_current]})
            
            # Concatenate the new data to the existing DataFrame
            data_frame = pd.concat([data_frame, new_data], ignore_index=True)
            
            # Print the received data
            print(new_data)
            # print(f"Timestamp: {timestamp:}")
            # print(f"Temperature: {temperature:.2f}")
            # print(f"Humidity: {humidity:.2f}")
            # print(f"Current: {psu_current:.3f}")
            
except Exception as e:
    print(e)
    # Save the data frame to a CSV file when the script is interrupted
    # data_frame.to_csv("sensor_data.csv", index=False)
    # ser.close()
