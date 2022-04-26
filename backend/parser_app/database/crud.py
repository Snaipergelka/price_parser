import logging
from . import models, schemas
from .database_config import SessionLocal

logger = logging.getLogger()


class CRUD:

    def __init__(self):
        db = SessionLocal()
        self.db = SessionLocal()

    def create_product(self, product: str):

        # Creating product ID and URL model.
        db_product = models.ProductsIDAndURL(**{"url": product})

        logger.info(f"Adding {product} to database.")
        self.db.add(db_product)

        # Committing database changes.
        self.db.commit()

        # Refreshing product ID and URL model.
        self.db.refresh(db_product)

        self.db.close()
        return db_product

    def create_product_info(self, product: schemas.ProductsInfoCreate, prod_id: int) -> object:

        # Creating product info model.
        db_product = models.ProductsInfo(**product.dict(), product_id=prod_id)

        logger.info(f"Adding {product} to database.")
        self.db.add(db_product)

        # Committing database changes.
        self.db.commit()

        # Refreshing product info model.
        self.db.refresh(db_product)

        self.db.close()
        return db_product

    def create_user(self, user: schemas.UserCreate):

        # Checking if user is already created.
        data = self.db.query(models.User).filter_by(phone_number=user.phone_number).first()
        if not data:

            # Creating user model.
            db_user = models.User(**user.dict())

            logger.info(f"Adding {user} to database.")
            self.db.add(db_user)

            # Committing database changes.
            self.db.commit()

            # Refreshing user model.
            self.db.refresh(db_user)

            self.db.close()
            return {"name": db_user.name, "phone_number": db_user.phone_number}

        self.db.close()
        return {"name": data.name, "phone_number": data.phone_number}

    def create_product_and_user(self, data: schemas.UsersAndProducts):

        # Creating user subscription model.
        db_user_product = models.UserAndProductID(**data.dict())

        logger.info(f"Adding user subscription {data} to database.")
        self.db.add(db_user_product)

        # Committing database changes.
        self.db.commit()

        # Refreshing user subscription model.
        self.db.refresh(db_user_product)

        self.db.close()
        return db_user_product

    def get_user(self, user: str):

        logger.info(f"Getting user by {user}.")
        data = self.db.query(models.User).filter_by(phone_number=user).first()

        self.db.close()
        if data:
            return data

    def get_product_by_url(self, url):

        logger.info(f"Getting product by {url}.")
        data = self.db.query(models.ProductsIDAndURL).filter_by(url=url).first()

        self.db.close()
        if data:
            return data.id

    def get_all_products_for_user_with_details(self, number: str):

        logger.info(f"Getting user subscriptions by phone {number}.")
        products = self.db.query(models.ProductsInfo).join(
            models.UserAndProductID).join(
            models.User, models.User.phone_number == number).all()
        self.db.close()
        return products

    def get_all_products_for_user_without_details(self, number: str):

        logger.info(f"Getting user by {number}.")
        products = self.db.query(models.UserAndProductID).join(
            models.User, models.User.phone_number == number).all()
        self.db.close()
        return [product.product_id for product in products]

    def get_product_by_user_id(self, user: schemas.UserInfo):

        logger.info(f"Getting product by {user.id}.")
        result = self.db.query(models.UserAndProductID).filter(
            models.UserAndProductID.user_id == user.id).all()
        self.db.close()
        return result

    def unsubscribe_product(self, user_and_prod: schemas.UsersAndProducts):

        logger.info(f"Unsubscribing {user_and_prod.user_id} from {user_and_prod.product_id}.")
        self.db.query(models.UserAndProductID).filter(
            models.UserAndProductID.user_id == user_and_prod.user_id).filter(
            models.UserAndProductID.product_id == user_and_prod.product_id).delete()

        # Commit changes to database.
        self.db.commit()

        self.db.close()
        return "Success"

    def delete_user(self, user_id: int):

        logger.info(f"Deleting {user_id} subscriptions ids from database.")
        self.db.query(models.UserAndProductID).filter(models.UserAndProductID.user_id == user_id).delete()
        self.db.commit()

        logger.info(f"Deleting {user_id} authentication data from database.")
        self.db.query(models.User).filter_by(id=user_id).delete()

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

    def update_information_about_product(self, product, name):
        # Creating product info model.

        logger.info(f"Updating {product} in database.")
        self.db.query(models.ProductsInfo).where(models.ProductsInfo.name == name).update(product)

        # Committing database changes.
        self.db.commit()

        self.db.close()
        return product
