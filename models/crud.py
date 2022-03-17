from sqlalchemy.orm import Session

from . import models, schemas


def get_product(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ProductsInfo).offset(skip).limit(limit).all()


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
