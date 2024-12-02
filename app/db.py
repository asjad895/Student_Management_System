from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import traceback

load_dotenv()


try:
    MONGO_URI = os.getenv("MONGO_URI")
    client = AsyncIOMotorClient(MONGO_URI)
    db = client["students_db"]
    print(f"Connected to Mongo Atlas Client ,db > {db.name}")
    # collections = db.list_collection_names
    # print(collections)
except Exception as e:
    exc = traceback.format_exception(e)
    print(exc)
