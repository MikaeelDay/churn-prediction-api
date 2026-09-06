# Customer Churn Prediction API

A production-style REST API built with **FastAPI** that predicts customer churn using a trained **Random Forest** classifier. Built as an end-to-end machine learning deployment project — from model training to a containerized, tested, authenticated API.

## Overview

Customer churn (customers leaving a service) is a critical metric for subscription-based businesses. This API takes a customer's profile (contract type, services subscribed, billing info, etc.) and predicts:

- Whether the customer is likely to churn (`Yes` / `No`)
- The probability of churn (a confidence score between 0 and 1)

The model is trained on the [Telco Customer Churn dataset](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) (7,043 customer records).

## Features

- **REST API** built with FastAPI, with interactive docs (Swagger UI) out of the box
- **ML model serving**: Random Forest classifier trained with scikit-learn
- **Input validation**: strict Pydantic schemas reject malformed requests before they reach the model
- **Authentication**: API key–based access control
- **Structured logging**: every prediction request and result is logged
- **Automated tests**: pytest test suite covering success, auth failure, and validation failure cases
- **Containerized**: fully Dockerized for consistent deployment
- **Clean architecture**: routers, schemas, ML logic, and auth are cleanly separated

## Tech Stack

| Layer          | Technology                  |
|----------------|------------------------------|
| API Framework  | FastAPI                     |
| ML             | scikit-learn (RandomForest) |
| Data Handling  | pandas, joblib               |
| Validation     | Pydantic                    |
| Testing        | pytest, httpx                |
| Containerization | Docker                    |
| Package Manager | uv                          |

## Project Structure

\```
ml-api/
├── app/
│   ├── routers/
│   │   └── predict.py       # /predict endpoint
│   ├── ml/
│   │   ├── train.py         # model training script
│   │   └── model.py         # model loading & inference logic
│   ├── schemas.py           # Pydantic request/response models
│   ├── auth.py               # API key authentication
│   └── logging_config.py     # logging setup
├── tests/
│   └── test_predict.py       # automated tests
├── data/
│   └── telco_churn.csv       # training dataset
├── models/
│   └── model.joblib           # trained model artifact
├── main.py                    # FastAPI app entry point
├── Dockerfile
├── pyproject.toml
└── README.md
\```

## Model

- **Algorithm**: Random Forest Classifier (100+ estimators)
- **Dataset**: Telco Customer Churn (7,043 rows, 19 features after cleaning)
- **Accuracy**: ~78.75% on held-out test data
- **Preprocessing**: Label encoding for categorical features, missing value handling for `TotalCharges`

To retrain the model:
\```bash
uv run python app/ml/train.py
\```

## Getting Started

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

\```bash
git clone https://github.com/MikaeelDay/churn-prediction-api.git
cd churn-prediction-api
uv sync
\```

### Running Locally

\```bash
uv run uvicorn main:app --reload
\```

The API will be available at `http://127.0.0.1:8000`. Interactive docs at `http://127.0.0.1:8000/docs`.

### Running with Docker

\```bash
docker build -t churn-api .
docker run -p 8000:8000 churn-api
\```

## API Usage

All prediction requests require an `X-API-Key` header.

### Example Request

\```bash
curl -X POST "http://127.0.0.1:8000/predict" \\
  -H "X-API-Key: my-secret-key-123" \\
  -H "Content-Type: application/json" \\
  -d '{
    "gender": "Female",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "tenure": 12,
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "InternetService": "Fiber optic",
    "OnlineSecurity": "No",
    "OnlineBackup": "Yes",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "Yes",
    "StreamingMovies": "No",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 70.35,
    "TotalCharges": 845.5
  }'
\```

### Example Response

\```json
{
  "churn_prediction": "Yes",
  "churn_probability": 0.575
}
\```

## Testing

\```bash
uv run pytest -v
\```

## Future Improvements

- Move the API key to an environment variable instead of hardcoding it (currently for demo purposes only)
- Upgrade to JWT-based authentication for multi-user support
- Add rate limiting
- Deploy to a cloud platform (Render/Railway) with CI/CD
- Experiment with additional models (XGBoost, LightGBM) and compare performance

## License

MIT