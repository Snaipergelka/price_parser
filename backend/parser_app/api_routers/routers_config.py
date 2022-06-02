from backend.parser_app.database import crud


def connecting_to_db():
    return crud.CRUD()
