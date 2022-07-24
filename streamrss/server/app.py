import asyncio
import os
from datetime import datetime
from typing import List

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi_sqlalchemy import DBSessionMiddleware, db
from sse_starlette.sse import EventSourceResponse
from streamrss.server import crud, models, schemas


BASE_DIR= os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(BASE_DIR, '.env'))

MESSAGE_STREAM_DELAY = 15  # second
MESSAGE_STREAM_RETRY_TIMEOUT = 15000  # milisecond

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])

@app.get("/")
async def root():
    return {"message": "hello world"}

@app.post('/stream/rules', response_model=schemas.Rules)
def rule(rule: schemas.RulesCreate):
    return crud.create_rule(db.session, rule)

@app.get('/stream/rules')
async def rule():
    rule = db.session.query(models.Rules).all()
    return {"rules": rule}

# TODO: use redis pubsub capabilities to publish new feeds to redis and implement
# logic to check if there are new messages and read them from redis if so
@app.get('/stream')
async def message_stream(request: Request):
    pass


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
