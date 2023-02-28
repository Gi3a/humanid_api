import face_recognition
import urllib.request as ur

from models.data import Data


class FaceRecognition:
    # def __init__(self,eth_conn, db_conn):
    def __init__(self, db_conn):
        # self.eth_conn = eth_conn
        self.db_conn = db_conn

    async def recognize_face(self, data: Data):
        # Base64 Image
        decoded = ur.urlopen(data.image)
        unknown_image = face_recognition.load_image_file(decoded)
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

        # MySQL
        conn = await self.db_conn.create_connection()
        person = await self.find_person_by_encoding(conn, unknown_encoding)

        if person:
            return {"person": person, "result": "match"}
        else:
            # Save to MySQL database with no name
            new_encoding = str(unknown_encoding.tolist())

            passport_address = None
            private_key_hash = None
            person = (passport_address, new_encoding)

            await self.create_person(conn, person)
            return {"person": person, "result": "not match"}

    async def create_person(self, conn, person):
        sql = ''' INSERT INTO domains(passport_address, face_encodings)
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
                    "passport_address": row[1],
                    "face_encodings": face_encodings
                }
        return None
