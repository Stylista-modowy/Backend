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

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = ["https://frontend-pi-blue.vercel.app", "http://localhost:5173", "*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/docs", include_in_schema=False)
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

@app.post("/wardrobe/add/")
async def add_items_to_wardrobe(items: List[schemas.WardrobeItemCreate], token: str, db: Session = Depends(database.get_db)):
    print(f'ITEMS: {items}')
    decoded_token = security.read_id_from_token(token=token)
    for item in items:
        print(item)
        crud.create_item(db=db, item=item, id=decoded_token)
    return {"message": "Items added to wardrobe"}

@app.get("/wardrobe/items/", response_model=List[Dict[str, Any]])
async def get_wardrobe_items(token: str, db: Session = Depends(database.get_db)):
    decoded_token = security.read_id_from_token(token=token)
    user = crud.get_user_by_id(db=db, id=decoded_token)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    items = crud.get_user_items(db=db, user_id=user.id)
    available_categories = crud.get_available_categories_for_user(db=db, id=user.id)

    categorized_items = []

    for category in available_categories:
        category_items = [item for item in items if item.item_category == category]
        categorized_items.append({"category": category, "items": category_items})

    return categorized_items

