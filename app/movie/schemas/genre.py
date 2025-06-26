from pydantic import BaseModel, Field


class GenreRead(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    name: str = Field(max_length=512)
    


class GenreReadMainPage(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    name: str 
    




