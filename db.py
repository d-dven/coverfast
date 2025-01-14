import certifi
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import certifi


# Load variables from .env file
load_dotenv()

uri = "mongodb+srv://newuser:newpassword@covercluster.mshnt.mongodb.net/?retryWrites=true&w=majority&appName=covercluster"
DATABASE_NAME = "coverdb"

client = None
_database = None 

async def connect_to_mongo():
    global client, _database
    try:
        client = MongoClient(uri, server_api=ServerApi(version='1', strict=True, deprecation_errors=True), tlsCAFile=certifi.where())
        _database = client[DATABASE_NAME]
        client.admin.command('ping')
        print("MongoDB connected!")
    except Exception as e:
        print(e)

def get_database():
    if _database is None:
        raise Exception("Database not initialized. Ensure connect_to_mongo is called before accessing the database.")
    return _database

async def close_mongo_connection():
    global client
    if client:
        client.close()
        print("MongoDB connection closed!")

