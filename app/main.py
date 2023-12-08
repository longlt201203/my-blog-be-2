from contextlib import asynccontextmanager, contextmanager
from dotenv import dotenv_values
from fastapi import FastAPI
from pymongo import MongoClient
from .controllers import posts_controller

config = dotenv_values()

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb_client = MongoClient(config["DB_CONNECTION_STRING"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to database.")
    yield

    app.mongodb_client.close()
    print("Disconnected to database.")

app = FastAPI(lifespan=lifespan)

app.include_router(posts_controller.router)