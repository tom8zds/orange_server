from typing import *

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session


SQLITE_URI = f'sqlite:///orange.sqlite'

engine = create_engine(SQLITE_URI, echo=True, future=True)
Base = declarative_base(engine)
session: Session = sessionmaker(engine)()