import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
df = pd.read_csv("../data/home_data.csv")

# Input features
X = df[["Temperature", "Light", "Motion"]]

# Target outputs
y_fan = df["Fan"]
y_light = df["LightLED"]
y_alarm = df["Alarm"]

# Train models
fan_model = RandomForestClassifier(random_state=42)
light_model = RandomForestClassifier(random_state=42)
alarm_model = RandomForestClassifier(random_state=42)

fan_model.fit(X, y_fan)
light_model.fit(X, y_light)
alarm_model.fit(X, y_alarm)

# Save models
joblib.dump(fan_model, "../model/fan_model.pkl")
joblib.dump(light_model, "../model/light_model.pkl")
joblib.dump(alarm_model, "../model/alarm_model.pkl")

print("✅ Models trained successfully!")