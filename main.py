from fastapi import FastAPI,Depends,HTTPException,Header
from pydantic import BaseModel
import asyncio
import time
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware


class UserIn(BaseModel):
    name: str
    age: int
    email: str
    password : str

class UserOut(BaseModel):
    name: str
    age: int
    email: str

app = FastAPI()

fake_users_db = {
    1 : "Ali",
    2 : "Reza",
}


@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in fake_users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user_id,
        "name": fake_users_db[user_id],
    }

@app.get("/")
def read_root():
    return {"message" : "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id : int):
    return {"item_id": item_id}

@app.get("/search")
def search_items(q: str = None, limit: int = None):
    return {
        "query" : q,
        "limit" : limit
    }


@app.post("/users/",response_model=UserOut)
def create_user(user : UserIn):
    return user


def verify_token(token: str = None):
    if token == "secret123":
        return {"authenticated": True}
    return {"authenticated": False}

@app.get("/protected")
def read_protected(params: dict = Depends(verify_token)):
    return params

@app.get("/slow-sync")
def slow_sync_endpoint():
    time.sleep(5)
    return {"message": "slow sync"}

@app.get("/slow-async")
async def slow_async_endpoint():
    await asyncio.sleep(3)
    return {"message": "slow async"}


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

""" Api handling """

API_KEY = "my-secret-key-123"

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key

@app.get("/secure-data")
def get_secure_data(api_key: str = Depends(verify_api_key)):
    return {"data" : "this information is secure"}
