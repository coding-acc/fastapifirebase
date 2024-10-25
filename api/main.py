from fastapi import FastAPI, HTTPException
import connection
from bson import ObjectId
from pydantic import BaseModel
from firebase_admin import credentials, initialize_app, db
from typing import Optional


class Device(BaseModel):
    humidity : str

appplication = FastAPI()
cred = credentials.Certificate("./credentials.json")
firebase_app = initialize_app(cred, {'databaseURL':'https://ect-water-default-rtdb.firebaseio.com/'})


appplication.get("/")
def index():
    return {"message": "CONNECTED"}

appplication.post("/post/{num}/{humidity}")
async def postData(num: str, humidity: Device):
    new_item_ref = db.reference(num).push()
    new_item_ref.set(humidity.dict())
    return{"id":new_item_ref.key, **humidity.dict()}
