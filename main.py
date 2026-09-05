import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routers import predict
from app.logging_config import setup_logging
setup_logging()
app = FastAPI(
    title="Customer Churn Prediction API",
    description="A FastAPI service that predicts customer churn using a trained Random Forest model.",
    version="1.0.0",
)

# اجازه دسترسی از فرانت‌اندهای دیگر (در صورت نیاز آینده)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(predict.router)