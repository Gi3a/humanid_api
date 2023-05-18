from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from controllers import (account_controller, authentication_controller)
from utils.cors import (ALLOWED_HEADERS, ALLOWED_METHODS, ALLOWED_ORIGINS)


# API
api: FastAPI = FastAPI(
    title="HumanAPI",
    description="Web API for decentralized identity verification system",
    version="1.0.0",
    contact={
        "name": "Gi3a",
        "url": "https://github.com/gi3a",
    },
    swagger_ui_parameters={
        "filter": True,
    },
)


# Enable CORS middleware
api.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=ALLOWED_METHODS,
    allow_headers=ALLOWED_HEADERS,
    allow_credentials=True,
)

# Controllers
api.include_router(account_controller)
api.include_router(authentication_controller)
