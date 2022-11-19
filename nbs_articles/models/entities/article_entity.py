from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import relationship

from util.database_connector import Base


class ArticleEntity(Base):
    __tablename__ = 'articles'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    date = Column(String)
    url = Column(String, unique=True)
    body = Column(String)

    labels = relationship("LabelEntity", back_populates="article")
    links = relationship("LinkEntity", back_populates="article")
