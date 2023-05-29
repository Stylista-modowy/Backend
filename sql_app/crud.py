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

    print(f'\n\n\ndbitem: {db_item}\n\n\n')

    print(db.add(db_item))
    print(db.commit())
    print(db.refresh(db_item))

    return db_item