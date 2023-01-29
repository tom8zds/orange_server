from sqlalchemy.orm import Session

from . import models, schemas


def get_download(db: Session, download_id: int):
    return db.query(models.Download).filter(models.Download.id == download_id).first()


def get_download_by_tv_id(db: Session, tv_id: str):
    return db.query(models.Download).filter(models.Download.tv_id == tv_id).first()


def get_downloads(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Download).offset(skip).limit(limit).all()


def create_download(db: Session, download: schemas.DownloadBase):
    db_download = models.Download(**download.dict())
    db.add(db_download)
    db.commit()
    db.refresh(db_download)
    return db_download