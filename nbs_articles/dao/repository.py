from sqlalchemy.orm import Session

from models.dto.article_dto import ArticleCreateDTO
from models.dto.label_dto import LabelCreateDTO
from models.dto.link_dto import LinkCreateDTO
from models.entities.article_entity import ArticleEntity
from models.entities.label_entity import LabelEntity
from models.entities.link_entity import LinkEntity


def get_articles(db: Session):
    return db.query(ArticleEntity).all()


def get_article_by_id(db: Session, article_id: int):
    article = db.query(ArticleEntity).filter(ArticleEntity.id == article_id)
    return article.first() if article is not None else None


def get_articles_by_label(db: Session, label: str):
    articles = db.query(ArticleEntity).filter(label in ArticleEntity.labels)
    return articles.all() if articles is not None else []


def get_articles_by_date(db: Session, date: str):
    articles = db.query(ArticleEntity).filter(ArticleEntity.date == date)
    return articles.all() if articles is not None else []


def check_article_url_existence_in_db(db: Session, article_url: str):
    exist_article = db.query(ArticleEntity).filter(ArticleEntity.url == article_url)
    return True if exist_article is not None else False


def create_article(article_dto: ArticleCreateDTO,
                   labels: list[LabelCreateDTO],
                   links: list[LinkCreateDTO],
                   db: Session):
    article_entity = ArticleEntity(
        date=article_dto.date,
        url=article_dto.url,
        body=article_dto.body,
        labels=[],
        links=[]
    )

    save_to_db(article_entity, db)

    article_entity_id = article_entity.id

    insert_labels(labels, article_entity_id, db)
    insert_links(links, article_entity_id, db)

    return article_entity


def insert_labels(label_dtos: list[LabelCreateDTO],
                  article_entity_id: int,
                  db: Session):
    for label_dto in label_dtos:
        label_entity = LabelEntity(
            label=label_dto.label,
            article_id=article_entity_id
        )
        save_to_db(label_entity, db)


def insert_links(link_dtos: list[LinkCreateDTO],
                 article_entity_id: int,
                 db: Session):
    for link_dto in link_dtos:
        link_entity = LinkEntity(
            link=link_dto.link,
            article_id=article_entity_id
        )
        save_to_db(link_entity, db)


def save_to_db(entity, db):
    db.add(entity)
    db.commit()
    db.refresh(entity)
