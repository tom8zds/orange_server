from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/search/{bangumi_name}")
async def read_item(bangumi_name):
    return {"bangumi_name": bangumi_name}