from datetime import datetime
from pydantic import BaseModel, ConfigDict


class MeasureUnitBase(BaseModel):
    name: str
    short_name: str


class MeasureUnitCreate(MeasureUnitBase):
    pass


class MeasureUnitRead(MeasureUnitBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    create_date: datetime
