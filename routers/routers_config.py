from models import crud


def connecting_to_db():
    return crud.CRUD()
