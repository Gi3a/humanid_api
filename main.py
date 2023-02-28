import os

from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# from services.ethereum import EthereumConnection
from services.database import DatabaseConnection
from services.recognition import FaceRecognition

from models.data import Data


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


class App:
    def __init__(self):
        # self.eth_conn = EthereumConnection(
        #     os.getenv("ETH_PRIVATE_KEY"),
        #     os.getenv("CONTRACT_ADDRESS")
        # )
        self.db_conn = DatabaseConnection(
            os.getenv("DB_HOST"),
            os.getenv("DB_USER"),
            os.getenv("DB_PASSWORD"),
            os.getenv("DB_NAME")
        )
        self.face_recognition = FaceRecognition(
            # self.eth_conn,
            self.db_conn
        )

    async def recognize_face(self, data: Data):
        result = await self.face_recognition.recognize_face(data)
        return result


app_obj = App()


@app.post("/api/recognize_face")
async def recognize_face(data: Data):
    result = await app_obj.recognize_face(data)
    return result
