from typing import Optional

from pydantic import BaseModel


class Dimensions(BaseModel):
    width: Optional[int]
    length: Optional[int]
    height: Optional[int]
    units: Optional[str]


class GPTDescriptionResponse(BaseModel):
    description: str
    dimensions: Dimensions
