from pydantic import BaseModel


class Face(BaseModel):
    face_image: str
