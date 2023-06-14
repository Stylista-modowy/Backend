from sqlalchemy.orm import Session

from . import models, schemas, security

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(db: Session, id: str):
    return db.query(models.User).filter(models.User.id == id).first()

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

def create_item(db: Session, item: schemas.WardrobeItemCreate, id: str):
    
    print(f'\n\n\nuser id: {id}\n\n\n\n')

    db_user = get_user_by_id(db=db, id=id)
    print(f'\n\n\nuser: {db_user}\n\n\n')
    if not db_user:
        return

    db_item = models.Wardrobe(
        item_image = item.item_image,
        item_category = item.item_category,
        item_usage = item.item_usage,
        item_pref_weather = item.item_pref_weather,
        user_id = id
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item

def get_available_categories_for_user(db: Session, id: str):
    return [category[0] for category in db.query(models.Wardrobe.item_category).filter(models.Wardrobe.user_id == id).distinct().all()]


def get_user_items(db: Session, user_id: int):
    return db.query(models.Wardrobe).filter(models.Wardrobe.user_id == user_id).all()

def remove_user_items(db: Session, item_id: int):
    db.query(models.Wardrobe).filter(models.Wardrobe.id == item_id).delete()
    db.commit()
