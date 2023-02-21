from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import face_recognition
import os
import urllib.request as ur
import sqlite3


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


class DataImage(BaseModel):
    image: str


class Data(BaseModel):
    first_name: str = ""
    last_name: str = ""
    image: str


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('faces.db')
    except sqlite3.Error as e:
        print(e)

    return conn


def create_person(conn, person):
    sql = '''CREATE TABLE IF NOT EXISTS people (
                id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                face_encodings TEXT
            );'''
    conn.execute(sql)

    sql = ''' INSERT INTO people(first_name,last_name,face_encodings)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, person)
    return cur.lastrowid


def find_person_by_encoding(conn, encoding):
    sql = ''' SELECT * FROM people '''
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        face_encodings = eval(row[3])
        results = face_recognition.compare_faces([face_encodings], encoding)
        if True in results:
            return {
                "id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "face_encodings": face_encodings
            }
    return None


@app.post("/api/recognize_face")
async def recognize_face(data: Data):

    # All Faces
    known_faces_dir = "./known_faces"
    known_faces = []

    # Base64 Image
    decoded = ur.urlopen(data.image)
    unknown_image = face_recognition.load_image_file(decoded)
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

    if len(unknown_encoding) == 0:
        # Save to SQLite database with no name
        conn = create_connection()
        with conn:
            person = ("", "", "")
            create_person(conn, person)
        return {"result": "Not Matched"}
    else:
        unknown_encoding = unknown_encoding[0]

    for file in os.listdir(known_faces_dir):
        image = face_recognition.load_image_file(
            os.path.join(known_faces_dir, file))
        face_encoding = face_recognition.face_encodings(image)[0]
        known_faces.append(face_encoding)

    results = face_recognition.compare_faces(known_faces, unknown_encoding)

    if True in results:
        # Find and return matching person from SQLite database
        conn = create_connection()
        with conn:
            person = find_person_by_encoding(conn, unknown_encoding)
        return person
    else:
        # Save to SQLite database with no name
        conn = create_connection()
        with conn:
            person = ("", "", str(unknown_encoding.tolist()))
            create_person(conn, person)
        return {"result": "Not Matched"}
