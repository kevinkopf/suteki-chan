from json.decoder import JSONDecodeError
from datamodels import *
from fastapi import FastAPI, Request, HTTPException
from pydantic import ValidationError

suteki = FastAPI()


@suteki.get("/")
def root():
    return {"message": "Suteki Chan says NYA!"}

@suteki.post("/")
async def post_request(request: Request):
    try:
        request_body = await request.json()
    except JSONDecodeError as e:
        print(e)
        raise HTTPException(status_code=400, detail="Bad Request")

    try:
        model = Model(event={'suteki_request_type': request.headers.get('X-Gitlab-Event'), **request_body})
        return model.event
    except ValidationError as e:
        print(e)
        raise HTTPException(status_code=400, detail="Bad Request")
