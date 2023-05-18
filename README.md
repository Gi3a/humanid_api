# HumanID API on FastAPI

## Installation
```
pip install -r ./requirements.txt
```

## Startup
```
uvicorn main:api --reload
uvicorn main:api --ssl-keyfile=/etc/ssl/private/nginx-selfsigned.key --ssl-certfile=/etc/ssl/certs/nginx-selfsigned.crt;

source venv/bin/activate
uvicorn main:api --uds /tmp/uvicorn.sock --ssl-keyfile=/etc/ssl/private/nginx-selfsigned.key --ssl-certfile=/etc/ssl/certs/nginx-selfsigned.crt;
```

## Save
```
pip freeze > requirements.txt
```