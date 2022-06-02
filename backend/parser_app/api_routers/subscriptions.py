import logging
from .routers_config import connecting_to_db
import backend.parser_app.parser
from ..celery_tasks import get_info_about_product
from fastapi import Depends, APIRouter
from backend.parser_app.database import schemas, crud

router = APIRouter(
    prefix="/subscription",
    tags=["subscription"],
    )

logger = logging.getLogger()


@router.post("/all_subscribed_products_with_details")
def show_all_subscribed_products_with_details(user: schemas.UserAuth,
                                              conn: crud.CRUD = Depends(connecting_to_db)):
    logger.info(f"Accepted {user} to show all products with details.")

    # Getting info about products to which user is subscribed.
    products = conn.get_all_products_for_user_with_details(number=user.phone_number)
    logger.info(f"Got info about {products} to which {user} is subscribed.")
    return products


@router.post("/all_subscribed_products_without_details")
def show_all_subscribed_products_without_details(user: schemas.UserAuth,
                                                 conn: crud.CRUD = Depends(connecting_to_db)):
    logger.info(f"Accepted {user} to show all products.")

    # Getting products to which user is subscribed.
    products = conn.get_all_products_for_user_without_details(number=user.phone_number)

    # Getting info about products to which user is subscribed.
    if products:
        logger.info(f"Got {products} id to which {user} is subscribed.")
        return products

    else:
        return {"message": "You have no products!"}


@router.post("/subscribe_to_product")
async def subscribe_to_product(user_and_product: schemas.CreateSubscription,
                               conn: crud.CRUD = Depends(connecting_to_db)):

    logger.info(f"Accepted {user_and_product.phone_number} to subscribe to {user_and_product.url}.")

    # Checking if url is sephora-url
    if not backend.parser_app.parser.check_sephora_url(user_and_product.url) or \
            backend.parser_app.parser.check_sephora_product_url(
                backend.parser_app.parser.get_product_html(user_and_product.url)):
        return {"message": "Please provide url of product from sephora shop!"}

    # Checking if type of product is chosen if needed.
    if not backend.parser_app.parser.check_choice_of_alternative(user_and_product.url):
        return {"message": "Please choose type of the product!"}

    # Getting user from database by phone number.
    user = conn.get_user(user=user_and_product.phone_number)

    # Checking if user is authorised.
    if not user:
        return {"message": "Please register yourself"}

    # Getting product id by url from database.
    product_id = conn.get_product_by_url(url=user_and_product.url)

    # Checking if user and product are not None.
    if user and product_id:

        # Checking if user has already subscribed to product.
        if conn.check_user_subscription(user_id=user.id, product_id=product_id):
            return {"message": "You've already subscribed to product."}

        conn.create_product_and_user(data=schemas.UsersAndProducts(product_id=product_id, user_id=user.id))
        logger.info(f"Subscribed {user} to {product_id}.")
        return {"message": "You are successfully subscribed to product."}

    elif user and not product_id:

        logger.info(f"Parsing all the information about the {user_and_product.url}.")
        product_info = get_info_about_product.delay(url=user_and_product.url)
        product_info = product_info.get()

        # Creating products schema with information.
        product_info_in_schema = schemas.ProductsInfoCreate(**product_info)

        # Pushing product url to database.
        product = conn.create_product(product=user_and_product.url)

        # Pushing product info to database.
        conn.create_product_info(product=product_info_in_schema, prod_id=product.id)

        # Pushing user subscription to product to database.
        conn.create_product_and_user(data=schemas.UsersAndProducts(product_id=product.id, user_id=user.id))
        logger.info(f"Added all the information about the {product}, {user} subscription to db.")
        return {"message": "You are successfully subscribed to new product."}


@router.post("/unsubscribe_product")
async def unsubscribe_product(user_and_product: schemas.UsersAndProducts,
                              conn: crud.CRUD = Depends(connecting_to_db)):
    logger.info(
        f"Accepted {user_and_product.user_id} to unsubscribe from the {user_and_product.product_id}."
    )
    return conn.unsubscribe_product(user_and_product)
