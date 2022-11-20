from pydantic import BaseModel, validator


class ArticleBaseDTO(BaseModel):
    date: str
    url: str
    body: str


class ArticleCreateDTO(ArticleBaseDTO):
    pass


class ArticleUpdateDTO(BaseModel):
    date: str | None
    url: str | None
    body: str | None
    labels: list[str] | None = []
    links: list[str] | None = []

    @validator("labels", pre=True, each_item=True)
    def get_label_value(cls, v):
        value = v.label
        return value

    @validator("links", pre=True, each_item=True)
    def get_link_value(cls, v):
        value = v.link
        return value


class ArticleDTO(ArticleUpdateDTO):
    id: int

    class Config:
        orm_mode = True