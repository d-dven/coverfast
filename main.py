from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from utils import generate_response
from contextlib import asynccontextmanager
from db import close_mongo_connection, connect_to_mongo, get_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print('Starting up')
    await connect_to_mongo()
    yield
    # Shutdown logic
    await close_mongo_connection()

app = FastAPI(lifespan=lifespan)


class UserInfo(BaseModel):
    username: str
    password: str


origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/insert")
def write_data():
    database = get_database()
    collection = database["userinfo"]
    collection.insert_one({"name": "John Doe"})
    
@app.get("/")
def readrot():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, name: str, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/items/")
async def create_item(item: str):
    return {"item": item}


@app.post("/login/submit")
async def login_submit(userInfo: UserInfo):
    print(userInfo.username)
    if userInfo.username == "admin" and userInfo.password == "secret":
        return {"message": "Login successful"}
    return {"message": "Invalid credentials"}

@app.post("/chatbot")
async def chatbot(input: str):
    response = generate_response(input)
    return {"response": response}