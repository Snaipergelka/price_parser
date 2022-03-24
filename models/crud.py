from sqlalchemy.orm import Session

from . import models, schemas


def get_all_products_for_user(number: str, db: Session):
    user = db.query(models.User).filter_by(phone_number=number).first()
    products = db.query(models.UserAndProductID).filter(models.UserAndProductID.user_id == user.id).all()
    products_info = []
    for product in products:
        products_info.extend(db.query(models.ProductsInfo).filter(models.ProductsInfo.product_id == product.product_id).all())
    return products_info


def get_product_for_user(db: Session, user_id: int, product_id: int):
    return bool(db.query(models.UserAndProductID).filter(models.UserAndProductID.user_id == user_id).filter(models.UserAndProductID.product_id == product_id).all())


def get_product_url(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ProductsIDAndURL).offset(skip).limit(limit).all()


def create_product(db: Session, product: schemas.ProductURLAndIDCreate):
    db_product = models.ProductsIDAndURL(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def create_product_info(db: Session, product: schemas.ProductsInfoCreate, prod_id: int) -> object:
    """

    :rtype: object
    """
    db_product = models.ProductsInfo(**product.dict(), product_id=prod_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def create_user(db: Session, user: schemas.UserCreate):
    data = db.query(models.User).filter_by(phone_number=user.phone_number).first()
    if not data:
        db_user = models.User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    return data


def find_user(db: Session, user: schemas.UserAuth):
    data = db.query(models.User).filter_by(phone_number=user.phone_number).first()
    if data:
        return data.id


def find_url(db: Session, url):
    data = db.query(models.ProductsIDAndURL).filter_by(url=url).first()
    if data:
        return data.id


def create_product_and_user(db: Session, data: schemas.UsersAndProducts):
    db_user_product = models.UserAndProductID(**data.dict())
    db.add(db_user_product)
    db.commit()
    db.refresh(db_user_product)
    return db_user_product
