from pydantic import BaseModel


class Dimensions(BaseModel):
    width: int
    length: int
    height: int
    units: str


class GPTDescriptionResponse(BaseModel):
    description: str
    dimensions: Dimensions
