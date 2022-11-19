from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import relationship

from util.database_connector import Base


class LinkEntity(Base):
    __tablename__ = 'links'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    link = Column(String)
    article_id = Column(Integer, ForeignKey("articles.id"))

    article = relationship("ArticleEntity", back_populates="links")
