from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from orange.core.database.database import Base

from orange.core.parser import parser
from orange.core.source import source
from orange.core.subscribe import subscribe
from orange.core.workflow import workflow

from orange.core.workflow import scheduler

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
orange.include_router(subscribe.router)
orange.include_router(workflow.router)

Base.metadata.create_all()

@orange.on_event("startup")
async def start_event():
    scheduler.scheduler.start()
    print("启动后台服务")