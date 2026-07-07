import serial
import pandas as pd
import os
import time

PORT = "COM4"      # Change this
BAUD = 9600

ser = serial.Serial(PORT, BAUD, timeout=1)

filename = "../data/home_data.csv"

if not os.path.exists(filename):
    df = pd.DataFrame(columns=["Temperature","Light","Motion"])
    df.to_csv(filename,index=False)

print("Collecting Data...")

while True:

    try:

        line = ser.readline().decode().strip()

        if line:

            print(line)

            values = line.split(",")

            if len(values)==3:

                df = pd.DataFrame([values],
                    columns=["Temperature","Light","Motion"])

                df.to_csv(filename,
                          mode='a',
                          header=False,
                          index=False)

    except KeyboardInterrupt:

        print("Stopped")

        break