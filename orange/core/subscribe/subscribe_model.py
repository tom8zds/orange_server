from orange.core.database.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, String, ForeignKey, UniqueConstraint

class Episode(Base):
    __tablename__ = "episode"
    __table_args__ = (
        UniqueConstraint("subscribe_id", "episode_number", name="ani_ep_idx"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    subscribe_id = Column(Integer, ForeignKey("subscribe.id"))
    anime_name = Column(String, nullable=False)
    season_number = Column(Integer)
    episode_number = Column(Integer)

    def __repr__(self):
        return f"Episode(id={self.id!r}, anime_id={self.anime_name!r}, season_number={self.season_number!r}, episode_number={self.episode_number!r})"

class Subscribe(Base):
    __tablename__ = "subscribe"
    __table_args__ = (
        UniqueConstraint("tv_id", "season_number", name="ani_db_idx"),
        UniqueConstraint("source_id", "provider_id", name="ani_src_idx"),
    )

    id= Column(Integer, primary_key=True, autoincrement=True)
    name= Column(String, nullable=False)
    status= Column(Integer)
    tv_id= Column(String, nullable=False)
    season_number= Column(Integer)
    source_id= Column(String, nullable=False)
    provider_id= Column(String, nullable=False)
    parse_param=Column(String)

    episodes = relationship("Episode", backref="subscribe")

    def __repr__(self):
        return f"Subscribe(id={self.id!r}, name={self.name!r})"

        
