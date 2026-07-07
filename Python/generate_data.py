import pandas as pd
import random

rows = []

for _ in range(2000):

    # Temperature between 18°C and 45°C
    temp = round(random.uniform(18, 45), 1)

    # Light sensor value
    light = random.randint(0, 1023)

    # Motion detected (0 or 1)
    motion = random.randint(0, 1)

    # Smart home rules
    fan = 1 if temp > 30 else 0
    light_led = 1 if light < 500 else 0
    alarm = 1 if motion == 1 else 0

    rows.append([
        temp,
        light,
        motion,
        fan,
        light_led,
        alarm
    ])

df = pd.DataFrame(rows, columns=[
    "Temperature",
    "Light",
    "Motion",
    "Fan",
    "LightLED",
    "Alarm"
])

df.to_csv("../data/home.csv", index=False)

print("Dataset generated successfully!")
print(df.head())