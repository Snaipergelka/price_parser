import logging

from sqlalchemy.orm import Session
import backend.parser
from backend.celery_tasks import get_info_about_product
from models.database import SessionLocal, engine
from fastapi import FastAPI, Depends
import uvicorn
from models import models, schemas, crud


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


logger = logging.getLogger()


class CRUD:

    def __init__(self):
        self.db_connection = self.get_db

    @staticmethod
    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()


@app.post("/user/registration/")
async def create_user(
        user: schemas.UserCreate,
        db: Session = Depends(CRUD().db_connection)):
    logger.info("Creating user")
    return crud.create_user(db=db, user=user)


@app.post("/subscribe_to_product/")
async def subscribe_to_product(
        user: schemas.UserAuth,
        product: schemas.ProductURLAndIDCreate,
        db: Session = Depends(CRUD().db_connection)):

    logger.info("Checking if type of product is chosen if needed.")
    if not backend.parser.check_choice_of_alternative(product.url):
        return "Please choose type of the product!"

    logger.info("Getting user from database by phone number.")
    user = crud.get_user(db=db, user=user)

    logger.info("Checking if user is authorised.")
    if not user:
        return "Please register yourself"

    logger.info("Getting product id by url from database.")
    product_id = crud.get_product_by_url(db=db, url=product.url)

    logger.info("Checking if user and product are not None.")
    if user and product_id:

        logger.info("Checking if user has already subscribed to product.")
        if crud.check_user_subscription(db=db, user_id=user.id, product_id=product_id):
            return "You already subscribed the product!"

        logger.info("Subscribing user to product.")
        crud.create_product_and_user(db=db, data=schemas.UsersAndProducts(db=db, product_id=product_id, user_id=user.id))
        return "Success"

    elif user and not product_id:

        logger.info("Parsing all the information about the product.")
        product_info = get_info_about_product(product.url)

        logger.info("Creating products schema with information.")
        product_info_in_schema = schemas.ProductsInfoCreate(
            name=product_info[0], full_price=product_info[1],
            price_with_card=product_info[2], price_on_sale=product_info[3])

        logger.info("Pushing product url to database.")
        product = crud.create_product(db=db, product=product)

        logger.info("Pushing product info to database.")
        crud.create_product_info(db=db, product=product_info_in_schema, prod_id=product.id)

        logger.info("Pushing user subscription to product to database.")
        crud.create_product_and_user(db=db, data=schemas.UsersAndProducts(product_id=product.id, user_id=user.id))
        return product_info_in_schema


@app.post("/user/all_subscribed_products/")
def show_all_subscribed_products(user: schemas.UserAuth,
                                 db: Session = Depends(CRUD().db_connection)):

    logger.info("Getting user from database.")
    user = crud.get_user(db=db, user=user)

    if user:
        logger.info("Getting products to which user is subscribed.")
        products = crud.get_product_by_user_id(db=db, user=user)

        logger.info("Getting info about products to which user is subscribed.")
        if products:
            products = crud.get_all_products_for_user(db=db, number=user.phone_number)
            return products

        else:
            return "You have no products!"

    else:
        return "Please register yourself!"


@app.delete("/user/unsubscribed_product/")
async def unsubscribe_product(
        user: schemas.UserCreate,
        product: schemas.ProductURLAndIDCreate,
        db: Session = Depends(CRUD().db_connection)):

    logger.info("Unsubscribing the product.")
    return crud.unsubscribe_product(db=db, user=user, product=product)


@app.delete("/delete_user/")
async def delete_user(
        user: schemas.UserAuth,
        db: Session = Depends(CRUD().db_connection)):

    logger.info("Deleting user.")
    return crud.delete_user(db=db, user=user)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
