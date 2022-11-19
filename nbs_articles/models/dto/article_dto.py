from pydantic import BaseModel

from models.dto.label_dto import LabelDTO
from models.dto.link_dto import LinkDTO


class ArticleBaseDTO(BaseModel):
    date: str
    url: str
    body: str


class ArticleCreateDTO(ArticleBaseDTO):
    pass


class ArticleDTO(ArticleBaseDTO):
    id: int
    labels: list[LabelDTO] = []
    links: list[LinkDTO] = []

    class Config:
        orm_mode = True
