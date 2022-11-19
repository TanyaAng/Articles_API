from pydantic import BaseModel


class LinkBaseDTO(BaseModel):
    link: str


class LinkCreateDTO(LinkBaseDTO):
    pass


class LinkDTO(LinkBaseDTO):
    class Config:
        orm_mode = True
