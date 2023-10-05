from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str

class PartialUser(BaseModel):
    name: Optional[str]