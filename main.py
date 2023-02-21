from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import face_recognition
import os
import base64


app = FastAPI()

# Allow requests from all origins
origins = ["*"]

# Enable CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def decode_base64_image(base64_string):
    image_data = base64.b64decode(base64_string)
    return image_data


class Data(BaseModel):
    image: bytes


@app.post("/api/recognize_face")
async def recognize_face(data: Data):

    print(data.image)

    # known_faces_dir = "./known_faces"
    # known_faces = []

    # for file in os.listdir(known_faces_dir):
    #     image = face_recognition.load_image_file(
    #         os.path.join(known_faces_dir, file))
    # face_encoding = face_recognition.face_encodings(image)[0]
    # known_faces.append(face_encoding)

    # image_bytes = base64.b64decode(data.image)
    # unknown_image = face_recognition.load_image_file(image_bytes)
    # unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

    # results = face_recognition.compare_faces(known_faces, unknown_encoding)

    # if True in results:
    #     return {"result": "Matched"}
    # else:
    #     return {"result": "Not Matched"}

    return {"status": "success"}
