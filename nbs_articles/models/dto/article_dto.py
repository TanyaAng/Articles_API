from pydantic import BaseModel, validator


class ArticleBaseDTO(BaseModel):
    date: str
    url: str
    body: str


class ArticleCreateDTO(ArticleBaseDTO):
    pass


class ArticleDTO(ArticleBaseDTO):
    id: int
    labels: list[str] = []
    links: list[str] = []

    @validator("labels", pre=True, each_item=True)
    def get_label_value(cls, v):
        value = v.label
        return value

    @validator("links", pre=True, each_item=True)
    def get_link_value(cls, v):
        value = v.link
        return value

    class Config:
        orm_mode = True
