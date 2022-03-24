import backend.parser
from backend.celery_tasks import get_info_about_product

from fastapi import Depends, FastAPI

import uvicorn

from sqlalchemy.orm import Session

from models import crud, models, schemas
from models.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/products/get_information/")
async def get_product_info(
        user: schemas.UserAuth,
        product: schemas.ProductURLAndIDCreate,
        db: Session = Depends(get_db)):
    if not backend.parser.check_choice_of_alternative(product.url):
        return "Please choose type of the product!"
    user_id = crud.find_user(db=db, user=user)
    product_id = crud.find_url(db=db, url=product.url)
    if user_id and product_id:
        if crud.get_product_for_user(db=db, user_id=user_id, product_id=product_id):
            return "You already subscribed the product!"
        crud.create_product_and_user(db=db, data=schemas.UsersAndProducts(product_id=product_id, user_id=user_id))
        return "Success"
    elif user_id and not product_id:
        product_info = get_info_about_product(product.url)
        product_info_in_schema = schemas.ProductsInfoCreate(
            name=product_info[0], full_price=product_info[1],
            price_with_card=product_info[2], price_on_sale=product_info[3])
        product = crud.create_product(db=db, product=product)
        crud.create_product_info(db=db, product=product_info_in_schema, prod_id=product.id)
        crud.create_product_and_user(db=db, data=schemas.UsersAndProducts(product_id=product.id, user_id=user_id))
        return product_info_in_schema
    if not user_id:
        return "Please register yourself"


@app.post("/products/")
def read_products(user: schemas.UserAuth, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(phone_number=user.phone_number).first()
    if user:
        products = db.query(models.UserAndProductID).filter(models.UserAndProductID.user_id == user.id).all()
        if products:
            products = crud.get_all_products_for_user(number=user.phone_number, db=db)
            return products
        else:
            return "You have no products!"
    else:
        return "Please register yourself!"


@app.post("/user/registration/")
async def create_user(
        user: schemas.UserCreate,
        db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
