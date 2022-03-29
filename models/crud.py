import logging
from sqlalchemy.orm import Session
from . import models, schemas

logger = logging.getLogger()


def create_product(db: Session, product: schemas.ProductURLAndIDCreate):

    logger.info("Creating product ID and URL model.")
    db_product = models.ProductsIDAndURL(**product.dict())

    logger.info("Adding product ID an URL to database.")
    db.add(db_product)

    logger.info("Committing database changes.")
    db.commit()

    logger.info("Refreshing product ID and URL model.")
    db.refresh(db_product)
    return db_product


def create_product_info(db: Session, product: schemas.ProductsInfoCreate, prod_id: int) -> object:

    logger.info("Creating product info model.")
    db_product = models.ProductsInfo(**product.dict(), product_id=prod_id)

    logger.info("Adding product info model.")
    db.add(db_product)

    logger.info("Committing database changes.")
    db.commit()

    logger.info("Refreshing product info model.")
    db.refresh(db_product)
    return db_product


def create_user(db: Session, user: schemas.UserCreate):

    logger.info("Checking if user is already created.")
    data = db.query(models.User).filter_by(phone_number=user.phone_number).first()
    if not data:

        logger.info("Creating user model.")
        db_user = models.User(**user.dict())

        logger.info("Adding user model.")
        db.add(db_user)

        logger.info("Committing database changes.")
        db.commit()

        logger.info("Refreshing user model.")
        db.refresh(db_user)
        return db_user

    return data


def create_product_and_user(db: Session, data: schemas.UsersAndProducts):

    logger.info("Creating user subscription model.")
    db_user_product = models.UserAndProductID(**data.dict())

    logger.info("Adding user subscription model.")
    db.add(db_user_product)

    logger.info("Committing database changes.")
    db.commit()

    logger.info("Refreshing user subscription model.")
    db.refresh(db_user_product)

    return db_user_product


def get_user(db: Session, user: schemas.UserAuth):

    logger.info("Getting user by phone number.")
    data = db.query(models.User).filter_by(phone_number=user.phone_number).first()
    if data:
        return data


def get_product_by_url(db: Session, url):

    logger.info("Getting product by url.")
    data = db.query(models.ProductsIDAndURL).filter_by(url=url).first()
    if data:
        return data.id


def get_all_products_for_user(number: str, db: Session):

    logger.info("Getting user by phone number.")
    user = db.query(models.User).filter_by(phone_number=number).first()

    logger.info("Getting products id by user id.")
    products = db.query(models.UserAndProductID).filter(models.UserAndProductID.user_id == user.id).all()
    products_info = []

    logger.info("Getting products info.")
    for product in products:
        products_info.extend(db.query(models.ProductsInfo).filter(models.ProductsInfo.product_id == product.product_id).all())

    return products_info


def get_product_by_user_id(db: Session, user: schemas.UserInfo):

    logger.info("Getting product by user id.")
    return db.query(models.UserAndProductID).filter(models.UserAndProductID.user_id == user.id).all()


def unsubscribe_product(db: Session, user: schemas.UserCreate,
                        product: schemas.ProductURLAndIDCreate):

    logger.info("Getting user by phone number.")
    user = db.query(models.User).filter_by(phone_number=user.phone_number).first()

    logger.info("Checking if user is registered.")
    if not user:
        return "Please register yourself!"

    logger.info("Getting product by url.")
    product = db.query(models.ProductsIDAndURL).filter_by(url=product.url).first()

    logger.info("Checking if product exists.")
    if not product:
        return "Product does not exist!"

    logger.info("Checking if user is subscribed to product by user and product ids.")
    prod_and_user = db.query(models.UserAndProductID).filter(
        models.UserAndProductID.user_id == user.id).filter(
        models.UserAndProductID.product_id == product.id).all()

    logger.info("Checking if there is subscription to product.")
    if prod_and_user:

        logger.info("Deleting subscription to product from database.")
        db.query(models.UserAndProductID).filter(models.UserAndProductID.user_id == user.id).filter(
            models.UserAndProductID.product_id == product.id).delete()

        logger.info("Commit changes to database.")
        db.commit()

        return "Success"

    return "You have already unsubscribed the product!"


def delete_user(db: Session, user: schemas.UserAuth):

    logger.info("Getting user by phone number.")
    user = db.query(models.User).filter_by(phone_number=user.phone_number).first()

    logger.info("Checking if user is registered.")
    if not user:
        return "You have already successfully deleted your data."

    logger.info("Getting user's subscriptions ids from database.")
    prod_and_user = db.query(models.UserAndProductID).filter(
        models.UserAndProductID.user_id == user.id).all()

    logger.info("Checking if there is user's subscriptions ids from database.")
    if prod_and_user:

        logger.info("Deleting user's subscriptions ids from database.")
        db.query(models.UserAndProductID).filter(models.UserAndProductID.user_id == user.id).delete()
        db.commit()

    logger.info("Deleting user authentication data from database.")
    db.query(models.User).filter_by(phone_number=user.phone_number).delete()

    logger.info("Commit changes to database.")
    db.commit()

    return "Success"


def check_user_subscription(db: Session, user_id: int, product_id: int):

    logger.info("Checking if there is any user's subscriptions.")
    return bool(db.query(models.UserAndProductID).filter(
        models.UserAndProductID.user_id == user_id).filter(
        models.UserAndProductID.product_id == product_id).all())
