from pydantic import BaseModel


class LabelBaseDTO(BaseModel):
    label: str


class LabelCreateDTO(LabelBaseDTO):
    pass


class LabelDTO(LabelBaseDTO):

    class Config:
        orm_mode = True