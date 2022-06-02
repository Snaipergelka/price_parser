import logging
from . import models, schemas
from .database import SessionLocal

logger = logging.getLogger()


class CRUD:

    def __init__(self):
        db = SessionLocal()
        self.db = db

    def create_product(self, product: schemas.ProductURLAndIDCreate):

        logger.info("Creating product ID and URL model.")
        db_product = models.ProductsIDAndURL(**product.dict())

        logger.info("Adding product ID an URL to database.")
        self.db.add(db_product)

        # Committing database changes.
        self.db.commit()

        logger.info("Refreshing product ID and URL model.")
        self.db.refresh(db_product)

        self.db.close()
        return db_product

    def create_product_info(self, product: schemas.ProductsInfoCreate, prod_id: int) -> object:

        logger.info("Creating product info model.")
        db_product = models.ProductsInfo(**product.dict(), product_id=prod_id)

        logger.info("Adding product info model.")
        self.db.add(db_product)

        # Committing database changes.
        self.db.commit()

        logger.info("Refreshing product info model.")
        self.db.refresh(db_product)

        self.db.close()
        return db_product

    def create_user(self, user: schemas.UserCreate):

        logger.info("Checking if user is already created.")
        data = self.db.query(models.User).filter_by(phone_number=user.phone_number).first()
        if not data:

            logger.info("Creating user model.")
            db_user = models.User(**user.dict())

            logger.info("Adding user model.")
            self.db.add(db_user)

            # Committing database changes.
            self.db.commit()

            # Refreshing user model.
            self.db.refresh(db_user)

            self.db.close()
            return db_user

        self.db.close()
        return data

    def create_product_and_user(self, data: schemas.UsersAndProducts):

        logger.info("Creating user subscription model.")
        db_user_product = models.UserAndProductID(**data.dict())

        logger.info("Adding user subscription model.")
        self.db.add(db_user_product)

        # Committing database changes.
        self.db.commit()

        logger.info("Refreshing user subscription model.")
        self.db.refresh(db_user_product)

        self.db.close()
        return db_user_product

    def get_user(self, user: schemas.UserAuth):

        logger.info("Getting user by phone number.")
        data = self.db.query(models.User).filter_by(phone_number=user.phone_number).first()

        self.db.close()
        if data:
            return data

    def get_product_by_url(self, url):

        logger.info("Getting product by url.")
        data = self.db.query(models.ProductsIDAndURL).filter_by(url=url).first()

        self.db.close()
        if data:
            return data.id

    def get_all_products_for_user_with_details(self, number: str):

        logger.info(f"Getting user subscriptions by phone {number}.")
        products = self.db.query(models.ProductsInfo).join(models.UserAndProductID).join(models.User, models.User.phone_number == number).all()

        #logger.info("Getting products id by user id.")
        #products = self.db.query(models.UserAndProductID).filter(models.UserAndProductID.user_id == user.id).all()
        #products_info = []

        #logger.info("Getting products info.")
        #for product in user:
            #products_info.extend(self.db.query(models.ProductsInfo).filter(models.ProductsInfo.product_id == product.product_id).all())

        self.db.close()
        return products

    def get_all_products_for_user_without_details(self, number: str):

        logger.info("Getting user by phone number.")
        products = self.db.query(models.UserAndProductID).join(models.User, models.User.phone_number == number).all()

        #logger.info("Getting products id by user id.")
        #products = self.db.query(models.UserAndProductID).filter(models.UserAndProductID.user_id == user.id).all()

        self.db.close()
        return [product.product_id for product in products]

    def get_product_by_user_id(self, user: schemas.UserInfo):

        logger.info("Getting product by user id.")
        result = self.db.query(models.UserAndProductID).filter(models.UserAndProductID.user_id == user.id).all()

        self.db.close()
        return result

    def unsubscribe_product(self, user_and_prod: schemas.UsersAndProducts):

        #logger.info("Getting user by phone number.")
        #user = self.db.query(models.User).filter_by(phone_number=user.phone_number).first()

        #logger.info("Checking if user is registered.")
        #if not user:
            #return "Please register yourself!"

        #logger.info("Getting product by url.")
        #product = self.db.query(models.ProductsIDAndURL).filter_by(url=product.url).first()

        #logger.info("Checking if product exists.")
        #if not product:
            #return "Product does not exist!"

        #logger.info("Checking if user is subscribed to product by user and product ids.")
        #prod_and_user = self.db.query(models.UserAndProductID).join(
         #   models.User, models.User.phone_number == user.phone_number).join(
          #  models.ProductsIDAndURL, models.ProductsIDAndURL.url == product.url).all()

        #logger.info("Checking if there is subscription to product.")
        #if prod_and_user:

            #logger.info("Deleting subscription to product from database.")
        self.db.query(models.UserAndProductID).filter(models.UserAndProductID.user_id == user_and_prod.user_id).filter(
            models.UserAndProductID.product_id == user_and_prod.product_id).delete()

        # Commit changes to database.
        self.db.commit()

        self.db.close()
        return "Success"

        #self.db.close()
        #return "You have already unsubscribed the product!"

    def delete_user(self, user: schemas.UserAuth):

        logger.info("Getting user by phone number.")
        user = self.db.query(models.User).filter_by(phone_number=user.phone_number).first()

        logger.info("Checking if user is registered.")
        if not user:
            return "You have already successfully deleted your data."

        #logger.info("Getting user's subscriptions ids from database.")
        #prod_and_user = self.db.query(models.UserAndProductID).filter(
            #models.UserAndProductID.user_id == user.id).all()

        #logger.info("Checking if there is user's subscriptions ids from database.")
        #if prod_and_user:

        logger.info("Deleting user's subscriptions ids from database.")
        self.db.query(models.UserAndProductID).filter(models.UserAndProductID.user_id == user.id).delete()
        self.db.commit()

        logger.info("Deleting user authentication data from database.")
        self.db.query(models.User).filter_by(phone_number=user.phone_number).delete()

        # Commit changes to database.
        self.db.commit()

        self.db.close()
        return "Success"

    def check_user_subscription(self, user_id: int, product_id: int):

        logger.info("Checking if there is any user's subscriptions.")
        result = bool(self.db.query(models.UserAndProductID).filter(
            models.UserAndProductID.user_id == user_id).filter(
            models.UserAndProductID.product_id == product_id).all())

        self.db.close()
        return result
