from pydantic import BaseModel


class Data(BaseModel):
    hex_address: str = ""
    image: str
