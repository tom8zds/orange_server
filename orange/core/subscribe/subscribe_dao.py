import json
from sqlalchemy.orm import Session

from . import subscribe_model, subscribe_schema
from fastapi.encoders import jsonable_encoder



def get_subscribe(db: Session, subscribe_id: int):
    return db.query(subscribe_model.Subscribe).filter(subscribe_model.Subscribe.id == subscribe_id).first()


def get_subscribe_by_tv_id(db: Session, tv_id: str):
    return db.query(subscribe_model.Subscribe).filter(subscribe_model.Subscribe.tv_id == tv_id).first()


def get_subscribes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(subscribe_model.Subscribe).offset(skip).limit(limit).all()


def create_subscribe(db: Session, subscribe: subscribe_schema.SubscribeCreate):
    data = subscribe.dict().copy()
    data["parse_param"] = json.dumps(jsonable_encoder(subscribe.parse_param))
    data["name"] = subscribe.parse_param.name
    db_subscribe = subscribe_model.Subscribe(**data)
    db.add(db_subscribe)
    db.commit()
    db.refresh(db_subscribe)
    return db_subscribe


def get_episodes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(subscribe_model.Episode).offset(skip).limit(limit).all()


def create_episode(db: Session, item: subscribe_schema.EpisodeCreate):
    db_item = subscribe_model.Episode(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item