import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
import joblib

# Load the dataset
df = pd.read_csv("activity_dataset.csv")

# Check the actual column names
print("Columns in the dataset:", df.columns)

# Initialize LabelEncoders
le_event = LabelEncoder()
le_ext = LabelEncoder()

# Ensure the column "event_type" exists or handle it
if "event_type" in df.columns:
    df["event_type_encoded"] = le_event.fit_transform(df["event_type"])
else:
    print("⚠️ 'event_type' column is missing. Adding a default column.")
    df["event_type"] = "default_event"  # Add a default value
    df["event_type_encoded"] = le_event.fit_transform(df["event_type"])

# Ensure the column "extension" exists or handle it
if "extension" in df.columns:
    df["extension_encoded"] = le_ext.fit_transform(df["extension"])
else:
    print("⚠️ 'extension' column is missing. Adding a default column.")
    df["extension"] = "default_ext"  # Add a default value
    df["extension_encoded"] = le_ext.fit_transform(df["extension"])

# Ensure the column "timestamp" exists or handle it
if "timestamp" in df.columns:
    df["hour"] = pd.to_datetime(df["timestamp"]).dt.hour
else:
    print("⚠️ 'timestamp' column is missing. Adding a default column.")
    df["timestamp"] = pd.Timestamp.now()  # Add a default timestamp
    df["hour"] = pd.to_datetime(df["timestamp"]).dt.hour

# Ensure the column "path_depth" exists or handle it
if "path_depth" not in df.columns:
    print("⚠️ 'path_depth' column is missing. Adding a default column.")
    df["path_depth"] = 1  # Add a default value for path depth

# Use selected features
X = df[["event_type_encoded", "path_depth", "extension_encoded", "hour"]]

# Train the Isolation Forest model
model = IsolationForest(contamination=0.05, random_state=42)
model.fit(X)

# Save the trained model and encoders
joblib.dump(model, "ransomware_model.pkl")
joblib.dump(le_event, "label_encoder_event.pkl")
joblib.dump(le_ext, "label_encoder_ext.pkl")

print("✅ ML Model trained and saved.")