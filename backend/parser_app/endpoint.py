import uvicorn
from fastapi import FastAPI
from backend.parser_app.api_routers import users, subscriptions
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - "
           "[%(levelname)s] - "
           "%(name)s - "
           "(%(filename)s).%(funcName)s(%(lineno)d) - "
           "%(message)s",
)

app = FastAPI()

app.include_router(users.router)
app.include_router(subscriptions.router)


if __name__ == "__main__":
    uvicorn.run(app)
