from fastapi import FastAPI,Depends,HTTPException,Header
from pydantic import BaseModel
import asyncio
import time
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

from app.routers import predict

app.include_router(predict.router)