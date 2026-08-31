import pandas as pd
from narwhals.selectors import categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os


def load_and_clean_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    df = df.drop(columns=["customerID"])
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

    df = df.dropna(subset=["TotalCharges"])

    return df


def train_and_save_model():
    df = load_and_clean_data("data/telco_churn.csv")

    Y = df["Churn"].map({
        "Yes" : 1,
        "No" : 0
    })

    X = df.drop(columns=["Churn"])

    categorical_cols = X.select_dtypes(include="object").columns.tolist()

    encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        encoders[col] = le

    X_train, X_test, y_train, y_test = train_test_split(
        X, Y, test_size=0.2, random_state=42, stratify=Y
    )

    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    print(f"Accuracy: {accuracy:.2%}")
    print("\n Classification report")
    print(classification_report(y_test, predictions))

    os.makedirs("models", exist_ok=True)
    joblib.dump({
        "model": model,
        "encoders": encoders,
        "feature_names": X.columns.tolist(),
    },"models/model.joblib")
    print("Model artifact saved to models/model.joblib")

if __name__ == "__main__":
    train_and_save_model()