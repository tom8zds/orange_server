from orange.core.database.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, String

class Download(Base):
    __tablename__ = "download"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # episode | season
    anime_id = Column(Integer, nullable=False)
    episode_id = Column(Integer, nullable=False, unique=True)
    mission_id = Column(String, nullable=False, unique=True)
    # Pause | Downloading | Seeding | Done | Failed
    status = Column(Integer, nullable=False)
    link = Column(String, nullable=False)

    def __repr__(self):
        return f"Download(id={self.id!r}, anime_id={self.anime_id!r}, episode_id={self.episode_id!r}, mission_id={self.mission_id!r})"