from sqlalchemy.orm import Session
from starlette.requests import Request

from dao import repository
from models.dto.article_dto import ArticleUpdateDTO


class ArticlesService:
    def __init__(self, db: Session):
        self.db = db

    def get_articles(self, request: Request, label: str | None = None, date: str | None = None):
        if not label and not date and not request.query_params:
            articles = repository.get_articles(self.db)
        elif label:
            articles = repository.get_articles_by_label(label, self.db)
        elif date:
            articles = repository.get_articles_by_date(date, self.db)
        else:
            raise ValueError("Not valid query parameter")

        return articles

    def get_article_by_id(self, article_id: str):
        if not self.is_digit(article_id):
            raise ValueError("Not valid id")

        article_id = int(article_id)
        return repository.get_article_by_id(article_id, self.db)

    def delete_article_by_id(self, article_id: str):
        if not self.is_digit(article_id):
            raise ValueError("Not valid id")

        article_id = int(article_id)
        return repository.delete_article_by_id(article_id, self.db)

    def update_article_by_id(self, article_id, body: ArticleUpdateDTO):
        if not self.is_digit(article_id):
            raise ValueError("Not valid id")

        article_id = int(article_id)
        return repository.update_article_by_id(article_id, body, self.db)

    def is_digit(self, article_id: str):
        return article_id.isdigit()