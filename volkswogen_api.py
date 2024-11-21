from flask import Flask, jsonify, request
import pandas as pd
import numpy as np
import pickle
from datetime import datetime

# Load the trained model
with open("trained_model.pkl", "rb") as f:
    model = pickle.load(f)

# Check if the model is properly fitted
if not hasattr(model, "predict"):
    raise ValueError("The model is not fitted!")

# Initialize Flask app
app = Flask(__name__)

# # Simulate real-time data stream (replace with actual stream source)
# def get_real_time_data():
#     # Simulate sensor readings and random variations
#     engine_temp = np.random.normal(75, 2)  # Normal engine temperature around 75C
#     brake_thickness = max(0, np.random.normal(12.0, 0.1))  # Brake thickness starting at 12mm
#     battery_voltage = np.random.normal(12.6, 0.05)  # Battery voltage around 12.6V
#     tire_pressure = np.random.normal(32.0, 1.0)  # Tire pressure in PSI
#     oil_quality = max(0, np.random.normal(100, 0.5))  # Oil quality percentage
#     cumulative_mileage = np.random.normal(5000, 50)  # Simulated mileage
#     driving_behavior = np.random.choice([0, 1, 2], p=[0.7, 0.2, 0.1])  # Normal, Aggressive, Conservative
#     environmental_condition = np.random.choice([0, 1], p=[0.8, 0.2])  # Good, Harsh environment

#     # Return simulated data in a dictionary
#     return {
#         "engine_temperature": engine_temp,
#         "brake_pad_thickness": brake_thickness,
#         "battery_voltage": battery_voltage,
#         "tire_pressure": tire_pressure,
#         "oil_quality": oil_quality,
#         "cumulative_mileage": cumulative_mileage,
#         "driving_behavior": driving_behavior,
#         "environmental_condition": environmental_condition
#     }

# Preprocess incoming real-time data
def hello_rout():
    return "Hello, World!"

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return hello_rout()


def preprocess_data(data):
    # Convert the categorical features to numerical values
    data["driving_behavior"] = data["driving_behavior"]
    data["environmental_condition"] = data["environmental_condition"]
    return pd.DataFrame([data])

# # API endpoint for real-time predictions
# @app.route('/api/predict', methods=['GET'])
# def predict_rul():
#     # Get real-time data
#     new_data = get_real_time_data()

#     # Preprocess the incoming data
#     new_data_df = preprocess_data(new_data)

#     # Make predictions using the model
#     predictions = model.predict(new_data_df)

#     # Extract the predicted RUL for each component
#     rul_brake, rul_battery, rul_oil, rul_tire = predictions[0]

#     # Get the current time for the prediction log
#     current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     # Prepare the response
#     response = {
#         "timestamp": current_time,
#         "predictions": {
#             "RUL_brake_pad": f"{rul_brake:.2f} days",
#             "RUL_battery": f"{rul_battery:.2f} days",
#             "RUL_oil": f"{rul_oil:.2f} days",
#             "RUL_tire": f"{rul_tire:.2f} days"
#         },
#         "input_data": new_data  # Include the input data for reference
#     }

#     return jsonify(response)


def get_real_time_data(data):
    # Simulate sensor readings and random variations
    engine_temp = data['engine_temp']
    brake_thickness = data['brake_thickness']
    battery_voltage = data['battery_voltage']
    tire_pressure = data['tire_pressure']
    oil_quality = data['oil_quality']
    cumulative_mileage = data['cumulative_mileage']
    driving_behavior = data['driving_behavior']
    environmental_condition = data['environmental_condition']

    # Return simulated data in a dictionary
    return {
        "engine_temperature": engine_temp,
        "brake_pad_thickness": brake_thickness,
        "battery_voltage": battery_voltage,
        "tire_pressure": tire_pressure,
        "oil_quality": oil_quality,
        "cumulative_mileage": cumulative_mileage,
        "driving_behavior": driving_behavior,
        "environmental_condition": environmental_condition
    }

@app.route('/api/predict', methods=['GET'])
def predict_rul():
    data = {
    "engine_temp": float(np.random.normal(75, 2)),  # Convert to standard Python float
    "brake_thickness":float(max(0, np.random.normal(12.0, 0.1))),
    "battery_voltage":float(np.random.normal(12.6, 0.05)),
    "tire_pressure":float(np.random.normal(32.0, 1.0)),
    "oil_quality":float(max(0, np.random.normal(100, 0.5))),
    "cumulative_mileage": float(np.random.normal(5000, 50)),
    "driving_behavior":int(np.random.choice([0, 1, 2], p=[0.7, 0.2, 0.1])),  # Convert to standard Python int
    "environmental_condition": int(np.random.choice([0, 1], p=[0.8, 0.2]))
    }
    # Get real-time data
    new_data = get_real_time_data(data)

    # Preprocess the incoming data
    new_data_df = preprocess_data(new_data)

    # Make predictions using the model
    predictions = model.predict(new_data_df)

    # Extract the predicted RUL for each component
    rul_brake, rul_battery, rul_oil, rul_tire = map(float, predictions[0])  # Convert to standard Python floats

    # Get the current time for the prediction log
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Prepare the response
    response = {
        "timestamp": current_time,
        "predictions": {
            "RUL_brake_pad": f"{rul_brake:.2f} days",
            "RUL_battery": f"{rul_battery:.2f} days",
            "RUL_oil": f"{rul_oil:.2f} days",
            "RUL_tire": f"{rul_tire:.2f} days"
        },
        "input_data": {k: float(v) if isinstance(v, np.float64) else int(v) if isinstance(v, np.int64) else v
                       for k, v in new_data.items()}  # Ensure input data is JSON serializable
    }

    return jsonify(response)


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
