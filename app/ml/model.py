import joblib
import pandas as pd
from functools import lru_cache

MODEL_PATH = "models/model.joblib"

class ChurnModel:
    def __init__(self, model_path: str):
        artifact = joblib.load(model_path)
        self.model = artifact['model']
        self.encoder = artifact['encoders']
        self.feature_names = artifact['feature_names']

    def predict(self, input_dict : dict) -> dict:
        df = pd.DataFrame([input_dict])

        for col,encoder in self.encoder.items():
            df[col] = encoder.transform(df[col])

        df = df[self.feature_names]

        prediction = self.model.predict(df)[0]
        probability = self.model.predict_proba(df)[0][1]

        return {
            "churn_prediction" : "Yes" if prediction == 1 else "No",
            "churn_probability" : round(float(probability), 4),
        }

@lru_cache()
def get_model() -> ChurnModel:
    return ChurnModel(MODEL_PATH)