from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from dao import repository
from models.dto import article_dto
from util import database_connector
from util.database_connector import SessionLocal, engine

# | Datapoint                | HTTP Method | Description                                   |
# | ------------------------ | ----------- | --------------------------------------------- |
# | /articles/               | GET         | get all crawled articles and their properties |
# | /articles/?label={label} | GET         | get list of articles with the same label      |
# | /articles/?date={date}   | GET         | get list of articles from the date            |
# | /article/{article_id}    | GET         | get single article                            |
# | /article/{article_id}    | DELETE      | delete single article                         |
# | /article/{article_id}    | PUT         | update single article                         |

app = FastAPI()
database_connector.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/articles/", response_model=list[article_dto.ArticleDTO])
def get_articles(db: Session = Depends(get_db)):
    articles = repository.get_articles(db)
    return articles

