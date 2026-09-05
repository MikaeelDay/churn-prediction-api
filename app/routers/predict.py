from fastapi import APIRouter, Depends
from app.schemas import ChurnInput, ChurnOutput
from app.ml.model import get_model, ChurnModel
from app.auth import verify_api_key
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/predict", response_model=ChurnOutput)
def predict_churn(data: ChurnInput,
                  model: ChurnModel = Depends(get_model),
                  api_key: str = Depends(verify_api_key)
                  ):
    logger.info(f"Received prediction request: tenure={data.tenure}, contract={data.Contract}")

    result = model.predict(data.model_dump())
    logger.info(f"Prediction result: {result['churn_prediction']} (probability={result['churn_probability']})")
    return result