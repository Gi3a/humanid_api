from pydantic import BaseModel


class Human(BaseModel):
    # Open
    public_key: str
    face_encodings: str
    # Closed
    personal_data: str
    encrypted_public_key: str
    encrypted_private_key: str
