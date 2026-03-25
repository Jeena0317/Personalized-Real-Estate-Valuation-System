from flask import Flask, request, render_template
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load model
model = joblib.load("models/real_estate_model.pkl")

# Load scaler (if used)
scaler = joblib.load("models/scaler.pkl")

# Feature list (must match training exactly)
feature_cols = [
    'bathroomcnt',
    'bedroomcnt',
    'calculatedfinishedsquarefeet',
    'lotsizesquarefeet',
    'yearbuilt',
    'garagecarcnt',
    'taxamount',
    'latitude',
    'longitude'
]

@app.route('/', methods=['GET', 'POST'])
def predict():
    prediction = None
    lower = None
    upper = None

    if request.method == 'POST':
        try:
            # Get input values
            data = {col: float(request.form[col]) for col in feature_cols}

            # Convert to DataFrame
            df = pd.DataFrame([data])

            # Apply scaling (only for selected columns)
            scaled_features = [
                'lotsizesquarefeet',
                'calculatedfinishedsquarefeet',
                'yearbuilt'
            ]
            df[scaled_features] = scaler.transform(df[scaled_features])

            # Prediction
            prediction = model.predict(df)[0]

            # Confidence interval (±10%)
            lower = prediction * 0.9
            upper = prediction * 1.1

        except Exception as e:
            print("Error:", e)

    return render_template(
        'index.html',
        prediction=prediction,
        lower=lower,
        upper=upper
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)