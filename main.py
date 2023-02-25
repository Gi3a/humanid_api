import os
import json
import asyncio
import aiomysql
import face_recognition
import urllib.request as ur

from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from utils.converter import face_encoding_to_address, address_to_face_encoding


app = FastAPI()

load_dotenv()

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


class Data(BaseModel):
    hex_address: str = ""
    image: str


class FaceRecognizer:
    def __init__(self, db_host, db_user, db_password, db_name):
        self.db_host = db_host
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name

    async def create_connection(self):
        try:
            conn = await aiomysql.connect(
                host=self.db_host,
                user=self.db_user,
                password=self.db_password,
                db=self.db_name
            )
            return conn
        except aiomysql.Error as e:
            print(e)
            raise e

    async def create_person(self, conn, person):
        sql = '''CREATE TABLE IF NOT EXISTS domains (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    hex_address VARCHAR(255),
                    face_encodings TEXT
                );'''
        async with conn.cursor() as cursor:
            await cursor.execute(sql)

        sql = ''' INSERT INTO domains(hex_address,face_encodings)
                  VALUES(%s,%s) '''
        async with conn.cursor() as cursor:
            await cursor.execute(sql, person)
            await conn.commit()
            return cursor.lastrowid

    async def find_person_by_encoding(self, conn, encoding):
        sql = ''' SELECT * FROM domains '''

        async with conn.cursor() as cursor:
            await cursor.execute(sql)
            rows = await cursor.fetchall()

        for row in rows:
            face_encodings = eval(row[2])
            results = face_recognition.compare_faces(
                [face_encodings], encoding)
            if True in results:
                return {
                    "id": row[0],
                    "hex_address": row[1],
                    "face_encodings": face_encodings
                }
        return None

    async def recognize_face(self, data: Data):
        # Base64 Image
        decoded = ur.urlopen(data.image)
        unknown_image = face_recognition.load_image_file(decoded)
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

        # MySQL
        conn = await self.create_connection()
        person = await self.find_person_by_encoding(conn, unknown_encoding)

        if person:
            return {"person": person, "result": "match"}
        else:
            # Save to MySQL database with no name
            new_encoding = str(unknown_encoding.tolist())
            person = (face_encoding_to_address(
                json.loads(new_encoding)), new_encoding)
            await self.create_person(conn, person)
            return {"person": person, "result": "not match"}


# create an instance of FaceRecognizer with database config from environment variables
face_recognizer = FaceRecognizer(
    os.getenv("DB_HOST"),
    os.getenv("DB_USER"),
    os.getenv("DB_PASSWORD"),
    os.getenv("DB_NAME")
)


@app.post("/api/recognize_face")
async def recognize_face(data: Data):
    result = await face_recognizer.recognize_face(data)
    return result
