from fastapi import FastAPI, HTTPException
import connection
from bson import ObjectId
from schematics.models import Model
from schematics.types import EmailType, StringType
from pydantic import BaseModel
from firebase_admin import credentials, initialize_app, db
from typing import Optional

#print(connection.check(url='https://github.com/'))

class Customer(Model):
    cust_id= ObjectId()
    cust_email = StringType(required=True)
    cust_name = StringType(required=True)

# An instance of class User
newuser = Customer()
class Device(BaseModel):
    #distance  : int
    humidity : str
    #pH : str
    #sensor : int
    
class GetData(BaseModel):
    data: int
    devID: str
    distance: int
    humidity: int
    ph: int
    sensor: int
    temperature: int  
    

# funtion to create and assign values to the instanse of class Customer created
def create_user(email, username):
    newuser.cust_id = ObjectId()
    newuser.cust_email  = email
    newuser.cust_name = username
    return dict(newuser)

app = FastAPI()
cred = credentials.Certificate("./credentials.json")
firebase_app = initialize_app(cred, {'databaseURL':'https://ect-water-default-rtdb.firebaseio.com/'})

# Our root endpoint
@app.get("/")
def index():
    return {"message": "CONNECTED"}


@app.post("/{num}}/")
async def uploadThis(num: str, device: Device):
    new_item_ref = db.reference(num).push()
    new_item_ref.set(device.dict())  
    return {"id":new_item_ref.key, **device.dict()}



@app.get("/data/{deviceID}")
async def service(deviceID: int):
    ref_item = db.reference('data')
    item = ref_item.get()
    if item:
        return{**item, "data": deviceID}
    else:
        raise HTTPException(status_code=404, detail="Item not found")




# Signup endpoint with the POST method
#@app.post("/signup/{email}/{username}")
#def addUser(email, username: str):
 #   user_exists = False
 #   data = create_user(email, username)

    # Covert data to dict so it can be easily inserted to MongoDB
 #   dict(data)

    # Checks if an email exists from the collection of users
  #  if connection.db.users.find(
   #     {'email': data['email']}
    #    ).count() > 0:
     #   user_exists = True
      #  print("Customer Exists")
       # return {"message":"Customer Exists"}
    # If the email doesn't exist, create the user
   # elif user_exists == False:
    #    connection.db.users.insert_one(data)
     #   return {"message":"User Created","email": data['email'], "name": data['name']}

#mongodb password: oDzRtMJJZrmpH8VV