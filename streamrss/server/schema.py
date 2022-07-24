from datetime import datetime
from pydantic import BaseModel

class Rules(BaseModel):
    id: int
    pattern: str
    tag: str
    time_created: datetime
    time_updated: datetime