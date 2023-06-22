import base64
import uvicorn
from enum import Enum
from PIL import Image
import numpy as np

import os

import uuid

from rembg import remove

import io

import random

from typing import List, Dict, Any

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas, database, security
from .database import SessionLocal, engine

from datetime import timedelta

from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.openapi.utils import get_openapi

from fastapi.middleware.cors import CORSMiddleware

from .image_crop import trim, put_on_image
from sql_app import ai

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FashionAi",debug=True)
origins = ["https://frontend-pi-blue.vercel.app", "http://localhost:5173", "*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/docs", include_in_schema=False, status_code = status.HTTP_200_OK)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="API documentation")

@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint():
    return JSONResponse(get_openapi(title="API documentation", version="1.0.0", routes=app.routes))

#---------------------

@app.post("/auth/signup/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/auth/signin/", response_model=schemas.Token)
async def login_for_access_token(
    form_data: schemas.UserLogin, db: Session = Depends(database.get_db)
):
    print(form_data)
    user = security.authenticate_user(
        db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data=crud.get_user_by_username(db=db, username=form_data.username).id, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# @app.post("/wardrobe/add/")
# async def add_item_to_wardrobe(item: schemas.WardrobeItemCreate, token: str, db: Session = Depends(database.get_db)):

#     crud.create_item(db=db, item=item, id=security.read_id_from_token(token=token))
#     return

a_c = [
"Long Sleeve Shirts",
"Short Sleeve Shirts",
"Tops",
"Trousers",
"Shorts",
"Dresses",
"Skirts",
"Shoes",
"Heels"
]

def return_wear_type(str: str):
    if str == a_c[0] or str == a_c[1] or str == a_c[2]:
        return 'Topwear'
    if str == a_c[3] or str == a_c[4] or str == a_c[5] or str == a_c[6]:
        return 'Bottomwear'
    if str == a_c[7] or str == a_c[8]:
        return 'Shoes'

@app.post("/wardrobe/add/")
async def add_items_to_wardrobe(items: List[schemas.WardrobeItemCreate], token: str, db: Session = Depends(database.get_db)):
    print(f'ITEMS: {len(items)}')
    decoded_token = security.read_id_from_token(token=token)
    print(token)
    for item in items:
        numbers = [int(x) for x in item.item_image.decode('utf-8').split(",")]
        byte_array = bytearray(numbers)
        image = Image.open(io.BytesIO(byte_array))

        print("\n\n\n")
        image = remove(image)
        image = trim(image)
        # print(image)
        print("\n\n\n")

        byte_array2 = io.BytesIO()
        # print(byte_array2)
        # print("\n\n\n")
        image.save(byte_array2, format='PNG')
        # print(image)
        # print("\n\n\n")
        byte_array2 = byte_array2.getvalue()
        numbers2 = ",".join(str(x) for x in byte_array2)
        # print(len(numbers2))
        # print("\n\n\n")
        item.item_image = numbers2.encode('utf-8')
        print(f'ITEM: {item.item_category}, {item.item_pref_weather}, {item.item_usage}, {len(item.item_image)}')
        # print("\n\n\n")
        generated_id = random.randint(1, 21474836)
        ai.upload_data_to_sql(generated_id, 'None', item.item_category, item.item_usage, item.item_pref_weather, return_wear_type(item.item_category), 'Female', item.item_image)
        crud.create_item(db=db, item=item, id=decoded_token)
    ai.generate_and_save_combinations()
    ai.load_combinations_from_csv_to_sql()
    return

# def convert_image_to_bytes(image):
#     output = io.BytesIO()
#     image.save(output, format='PNG')
#     image_bytes = output.getvalue()
#     uint8_array = ','.join(str(byte) for byte in image_bytes)
#     uint8_array = uint8_array.strip(',')  # Remove leading and trailing commas
#     return uint8_array


@app.get("/wardrobe/items/", response_model=List[Dict[str, Any]])
async def get_wardrobe_items(token: str, db: Session = Depends(database.get_db)):
    decoded_token = security.read_id_from_token(token=token)
    user = crud.get_user_by_id(db=db, id=decoded_token)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    items = crud.get_user_items(db=db, user_id=user.id)

    categorized_items = []

    for category in a_c:
        category_items = [item for item in items if item.item_category == category]
        categorized_items.append({"category": category, "items": category_items})

    return categorized_items

@app.get("/wardrobe/categories/", response_model=List[str])
async def get_categories(token: str, db: Session = Depends(database.get_db)):
    decoded_token = security.read_id_from_token(token=token)
    user = crud.get_user_by_id(db=db, id=decoded_token)

    return a_c

@app.delete("/wardrobe/remove/")
async def item_to_remove(token: str, items: List[int], db: Session = Depends(database.get_db)):
    decoded_token = security.read_id_from_token(token=token)
    user = crud.get_user_by_id(db=db, id=decoded_token)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for id in items:
        crud.remove_user_items(db=db, item_id = id, ai_id=crud.get_ai_id_by_id(db=db, item_id=id))
    # ai.update_weight_in_sql() TODO
    return

class Gender(Enum):
    Male = "Male",
    Female = "Female"

@app.post("/generate/")
async def generate(token: str, req: schemas.GenerateRequest, db: Session = Depends(database.get_db)):
    decoded_token = security.read_id_from_token(token=token)
    combiantion_id = ai.draw_combination_id()
    items = crud.get_combination_items(db=db, id=combiantion_id)
    tpose = None
    gender = None
    script_path = os.path.dirname(__file__)
    if req.back == "female":
        tpose = Image.open(os.path.join(script_path,'femaleT-pose.jpeg'))
        gender = "Female"
    elif req.back == "male":
        tpose = Image.open(os.path.join(script_path,'maleT-pose.jpeg'))
        gender = "Male"

    img = None

    c = 0
    for item in items:
        numbers = [int(x) for x in item[9].decode('utf-8').split(",")]
        byte_array = bytearray(numbers)
        image = Image.open(io.BytesIO(byte_array))
        print(item[3])
        if c == 0:
            img = put_on_image(image, tpose, gender, item[3])
        else:
            img = put_on_image(image, img, gender, item[3])
        c+=1
    byte_array2 = io.BytesIO()
    # print(byte_array2)
    # print("\n\n\n")
    img.save(byte_array2, format='PNG')
    # print(image)
    # print("\n\n\n")
    byte_array2 = byte_array2.getvalue()
    numbers2 = ",".join(str(x) for x in byte_array2)
    # print(len(numbers2))
    # print("\n\n\n")
    img = numbers2.encode('utf-8')
    #TODO ai skrypt xD
    # operate with image_crop
    return img

@app.post("/fav/")
async def fav(token: str, item: schemas.FavItem, db: Session = Depends(database.get_db)):
    decoded_token = security.read_id_from_token(token=token)
    crud.add_to_fav(db=db, id = decoded_token, item = item)
    return

@app.get("/fav/get/", response_model=List[schemas.FavItem])
async def fav(token: str, item: schemas.FavItem, db: Session = Depends(database.get_db)):
    decoded_token = security.read_id_from_token(token=token)
    return crud.get_fav_items(db=db, id=decoded_token)
