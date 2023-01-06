from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from orange.parser import parser
from orange.source import source

orange = FastAPI()

orange.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@orange.get("/")
async def root():
    return {"message": "Hello World"}

@orange.get("/status")
async def status():
    return {"status": 1}

orange.include_router(parser.router)
orange.include_router(source.router)
