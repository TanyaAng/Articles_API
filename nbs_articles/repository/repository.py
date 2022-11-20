from sqlalchemy.orm import Session

from models.dto.article_dto import ArticleCreateDTO, ArticleUpdateDTO
from models.dto.label_dto import LabelCreateDTO
from models.dto.link_dto import LinkCreateDTO
from models.entities.article_entity import ArticleEntity
from models.entities.label_entity import LabelEntity
from models.entities.link_entity import LinkEntity


def get_articles(db: Session):
    return db.query(ArticleEntity).all()


def get_article_by_id(article_id: int, db: Session):
    query_set = db.query(ArticleEntity).filter(ArticleEntity.id == article_id)
    return query_set.first() if query_set is not None else None


def get_articles_by_label(label: str, db: Session):
    filtered_articles = []
    [filtered_articles.append(a) for a in get_articles(db) if label in [lbl.label for lbl in a.labels]]
    return filtered_articles


def get_articles_by_date(date: str, db: Session):
    query_set = db.query(ArticleEntity).filter(ArticleEntity.date == date)
    return query_set.all() if query_set is not None else []


def check_article_url_existence_in_db(db: Session, article_url: str):
    query_set = db.query(ArticleEntity).filter(ArticleEntity.url == article_url)
    return True if query_set.first() is not None else False


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


def delete_article_by_id(article_id: int, db: Session):
    query_set = db.query(ArticleEntity).filter(ArticleEntity.id == article_id)
    deleted_article = query_set.first()

    if not deleted_article:
        return False

    db.delete(deleted_article)
    db.commit()

    return True


def update_article_by_id(article_id: int, body: ArticleUpdateDTO, db: Session):
    query_set = db.query(ArticleEntity).filter(ArticleEntity.id == article_id)
    updated_article = query_set.first()

    if not updated_article:
        return

    labels_dto_as_str = body.__dict__["labels"]
    if labels_dto_as_str:
        map_to_label_entities(body, labels_dto_as_str)

    links_dto_as_str = body.__dict__["links"]
    if links_dto_as_str:
        map_to_link_entities(body, links_dto_as_str)

    for key, value in body.__dict__.items():
        if value:
            setattr(updated_article, key, value)

    save_to_db(updated_article, db)

    return updated_article


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


def map_to_link_entities(body, links_dto_as_str):
    link_entities = []
    for link in links_dto_as_str:
        link_entity = LinkEntity(link=link)
        link_entities.append(link_entity)
    body.__dict__["links"] = link_entities


def map_to_label_entities(body, labels_dto_as_str):
    label_entities = []
    for label in labels_dto_as_str:
        label_entity = LabelEntity(label=label)
        label_entities.append(label_entity)
    body.__dict__["labels"] = label_entities
