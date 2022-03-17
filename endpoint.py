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


#@app.post("/products/get_url/", response_model=schemas.ProductURLAndID)
#async def get_url(
#        product: schemas.ProductURLAndIDCreate,
 #       db: Session = Depends(get_db)):
  #  return crud.create_product(db=db, product=product)


@app.post("/products/get_information/", response_model=schemas.ProductsInfoCreate)
async def get_product_info(
        product: schemas.ProductURLAndIDCreate,
        db: Session = Depends(get_db)):
    product_info = get_info_about_product(product.url)
    product_info_in_schema = schemas.ProductsInfoCreate(
        name=product_info[0], full_price=product_info[1],
        price_with_card=product_info[2], price_on_sale=product_info[3])
    product = crud.create_product(db=db, product=product)
    crud.create_product_info(db=db, product=product_info_in_schema, prod_id=product.id)
    return product_info_in_schema


@app.get("/products/", response_model=list[schemas.ProductInfo])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_product(db, skip=skip, limit=limit)
    return products


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
