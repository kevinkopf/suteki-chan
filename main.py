from datamodels import *
from receivers import *
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from json.decoder import JSONDecodeError
import os
from processors import PayloadProcessor
from pydantic import ValidationError
import sys
import yaml

suteki = FastAPI()
config = {}


@suteki.on_event("startup")
async def startup_event():
    global config
    config_path = os.getenv('SUTEKI_CONFIG')

    try:
        with open('./config.yaml') as f:
            config_local = yaml.load(f, Loader=yaml.BaseLoader)
        with open(str(config_path)) as f:
            config_user = yaml.load(f, Loader=yaml.BaseLoader)
    except yaml.YAMLError:
        print('ERROR: Could not read config file: ' + config_path)
    except FileNotFoundError:
        print('ERROR: Config file does not exist: ' + config_path)
    config = config_local | config_user
    if config['security']['token'] == "":
        print("ERROR: Security token not defined in config file: " + config_path)
        sys.exit()


@suteki.middleware('http')
async def catch_request(request: Request, call_next):
    receiver = determine_receiver(request).receiver
    if receiver.security_check(config['security']['token']):
        request = await modify_request_body(request)
        response = await call_next(request)
        return response
    return JSONResponse(status_code=401, content="Unauthorized")


def determine_receiver(request: Request) -> Receiver:
    user_agent = 'Custom'
    if request.headers.get('User-Agent')[:7] == 'GitLab/':
        user_agent = 'GitLab'
    return Receiver(receiver=dict(request.headers) | {'user_agent': user_agent})


async def modify_request_body(request: Request):
    try:
        request.state.event = {'type': request.headers.get('X-Gitlab-Event')}
        return request
    except JSONDecodeError as e:
        print(e)
        raise HTTPException(status_code=400, detail="Bad Request")


@suteki.get("/")
def root():
    return {"message": "Suteki Chan says NYA!"}


@suteki.post("/")
async def post_request(request: Request):
    try:
        request_body = await request.json()
        model = Model(model=request.state.event | request_body).model
        PayloadProcessor(config=config, model=model)
        return JSONResponse(content='{}')
    except ValidationError as e:
        print(e)
        raise HTTPException(status_code=400, detail="Bad Request")
    except JSONDecodeError as e:
        print(e)
        raise HTTPException(status_code=400, detail="Bad Request")
