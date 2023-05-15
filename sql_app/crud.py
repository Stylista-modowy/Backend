from sqlalchemy.orm import Session

from . import models, schemas, security

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(
        email=user.email, hashed_password=hashed_password, username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_item(db: Session, item: schemas.WardrobeItemCreate, email: str):
    
    db_user = get_user_by_email(db=db, email=email)
    
    db_item = models.Wardrobe(
        item_image = item.item_image,
        item_name = item.item_name,
        item_category = item.item_category,
        item_tags = item.item_tags,
        item_pref_weather = item.item_pref_weather,
        user_id = db_user.id
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item