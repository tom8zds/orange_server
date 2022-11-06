from fastapi import FastAPI

from dev_config import api_key
import tmdbsimple as tmdb
tmdb.API_KEY = api_key

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/search/{bangumi_name}")
async def read_item(bangumi_name):
    return {"bangumi_name": bangumi_name}