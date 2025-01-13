from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from utils import generate_response


class UserInfo(BaseModel):
    username: str
    password: str



app = FastAPI()

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