import joblib
import pandas as pd

model = joblib.load("accident_risk_model.pkl")
columns = joblib.load("model_columns.pkl")

def predict_accident(input_data):
    df = pd.DataFrame([input_data])
    df = pd.get_dummies(df)

    for col in columns:
        if col not in df.columns:
            df[col] = 0

    df = df[columns]

    # Get probability instead of 0/1
    probability = model.predict_proba(df)[0][1]   # probability of class 1

    # Convert to percentage score
    score = round(probability * 100, 2)


    return score