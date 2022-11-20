from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.requests import Request

from models.dto.article_dto import ArticleDTO, ArticleUpdateDTO
from service.articles_service import ArticlesService
from util import database_connector
from util.database_connector import engine, SessionLocal

SUCCESSFULLY_DELETED_MESSAGE = "Article has been successfully deleted"
RESOURCE_NOT_FOUND_MESSAGE = "Resource not found"
NOT_VALID_ID_MESSAGE = "Please enter valid id"
NOT_VALID_QUERY_PARAMETER_MESSAGE = "Please use valid query parameters"
URL_EXIST_MESSAGE = "URL already exists"

database_connector.Base.metadata.create_all(bind=engine)

app = FastAPI()
db = SessionLocal()
service = ArticlesService(db)


@app.get("/articles/", response_model=list[ArticleDTO])
def get_articles(request: Request, label: str | None = None, date: str | None = None):
    try:
        articles = service.get_articles(request, label, date)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=NOT_VALID_QUERY_PARAMETER_MESSAGE)

    if not articles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=RESOURCE_NOT_FOUND_MESSAGE)
    return articles


@app.get("/articles/{article_id}", response_model=ArticleDTO)
def get_article_by_id(article_id: str):
    try:
        article = service.get_article_by_id(article_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=NOT_VALID_ID_MESSAGE)

    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=RESOURCE_NOT_FOUND_MESSAGE)
    return article


@app.delete("/articles/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article_by_id(article_id: str):
    try:
        is_deleted = service.delete_article_by_id(article_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=NOT_VALID_ID_MESSAGE)

    if not is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=RESOURCE_NOT_FOUND_MESSAGE)
    return JSONResponse(content={"detail": SUCCESSFULLY_DELETED_MESSAGE})


@app.put("/articles/{article_id}", response_model=ArticleDTO, status_code=status.HTTP_201_CREATED)
def update_article_by_id(article_id: str, body: ArticleUpdateDTO):
    try:
        updated_article = service.update_article_by_id(article_id, body)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=NOT_VALID_ID_MESSAGE)
    except AttributeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=URL_EXIST_MESSAGE)

    if not updated_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=RESOURCE_NOT_FOUND_MESSAGE)
    return updated_article
