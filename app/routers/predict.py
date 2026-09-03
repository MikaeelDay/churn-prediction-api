from fastapi import APIRouter, Depends
from app.schemas import ChurnInput, ChurnOutput
from app.ml.model import get_model, ChurnModel
from app.auth import verify_api_key

router = APIRouter()

@router.post("/predict", response_model=ChurnOutput)
def predict_churn(data: ChurnInput,
                  model: ChurnModel = Depends(get_model),
                  api_key: str = Depends(verify_api_key)
                  ):
    result = model.predict(data.model_dump())
    return result