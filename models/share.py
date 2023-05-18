from pydantic import BaseModel


class Share(BaseModel):
    receiver: str
    human_id: str
    shared_id: str
    data: str


class Ban(BaseModel):
    human_id: str
    shared_id: str
