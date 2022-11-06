from fastapi import FastAPI

from dev_config import api_key
import tmdbsimple as tmdb
tmdb.API_KEY = api_key

app = FastAPI()

def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/search/{bangumi_name}")
async def read_item(bangumi_name:str):
    assert(len(bangumi_name) > 3)
    search = tmdb.Search()
    response = search.tv (query=bangumi_name, language="zh", include_adult=True)
    # for s in search.results:
    #     write_log(s['title'], s['id'], s['release_date'], s['popularity'])
    return response