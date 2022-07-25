from typing import Optional

from datetime import datetime
from pydantic import BaseModel

class RulesBase(BaseModel):
    pattern: str
    tag: str

    class Config:
        orm_mode = True

class Rules(RulesBase):
    id: int
    time_created: Optional[datetime]
    time_updated: Optional[datetime]

    class Config:
        orm_mode = True


class RulesCreate(RulesBase):
    pass
