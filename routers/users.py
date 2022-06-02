import logging
from fastapi import Depends, APIRouter
from models import schemas, crud
from .routers_config import connecting_to_db

logger = logging.getLogger()


router = APIRouter(
    prefix="/user",
    tags=["user"],
    )


@router.post("/registration")
async def create_user(user: schemas.UserCreate, conn: crud.CRUD = Depends(connecting_to_db)):
    logger.info(f"Accepted {user} to create.")
    return conn.create_user(user=user)


@router.delete("/delete_user")
async def delete_user(user_id: int,
                      conn: crud.CRUD = Depends(connecting_to_db)):
    logger.info(f"Accepted {user_id} to delete.")
    return conn.delete_user(user_id=user_id)
