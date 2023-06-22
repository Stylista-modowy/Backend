from sqlalchemy.orm import Session

from . import models, schemas, security
from sqlalchemy import text

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
    print(f'ITEM: {item.item_category}, {item.item_pref_weather}, {item.item_usage}, {len(item.item_image)}\n')
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

def get_ai_id_by_id(db: Session, item_id: int):
    return db.query(models.Wardrobe).filter(models.Wardrobe.id == item_id).first().ai_wardrobe_id

def remove_user_items(db: Session, item_id: int, ai_id: int):
    db.query(models.Wardrobe).filter(models.Wardrobe.id == item_id).delete()
    query = text('DELETE FROM wardrobe_test WHERE wardrobe_test.item_id = :id')
    result = db.execute(query, params={'id': id})
    db.commit()

# def add_to_fav(db: Session, id: int, item: schemas.FavItem):
#     db_item = models.Favs(
#         image = item.image,
#         user_id = id
#     )

#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)

#     return db_item

# def get_fav_items(db: Session, id: int):
#     return db.query(models.Favs).filter(models.Wardrobe.user_id == id).all()

def get_combination_items(db: Session, id: int):
    query = text('SELECT topwear_id, bottomwear_id, shoes_id FROM stylista.wages WHERE wages.idwages = :id')

    result = db.execute(query, params={'id': id})
    items = result.fetchone()
    # print(items)

    query = text('SELECT * FROM stylista.wardrobe_test WHERE wardrobe_test.item_id = :id')
    item1 = db.execute(query, params={'id': items[0]}).fetchone()
    query = text('SELECT * FROM stylista.wardrobe_test WHERE wardrobe_test.item_id = :id')
    item2 = db.execute(query, params={'id': items[1]}).fetchone()
    query = text('SELECT * FROM stylista.wardrobe_test WHERE wardrobe_test.item_id = :id')
    item3 = db.execute(query, params={'id': items[1]}).fetchone()

    # print(item1, item2, item3)

    to_return = (item1, item2, item3)
    #print(to_return)

    return to_return