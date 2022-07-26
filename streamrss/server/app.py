import os

import nats
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi_sqlalchemy import DBSessionMiddleware, db
from sse_starlette.sse import EventSourceResponse
from streamrss.server import crud, models, schemas

BASE_DIR= os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(BASE_DIR, '.env'))

MESSAGE_STREAM_DELAY = 1  # second
MESSAGE_STREAM_RETRY_TIMEOUT = 15000  # milisecond
NATS_SERVER_URL = os.environ['NATS_SERVER_URL']
FEED_SUBSCRIPTION_SUBJECT = os.environ['FEED_SUBSCRIPTION_SUBJECT']

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

def get_messages(pubsub):
    while True:
        message = pubsub.get_message()
        if message:
            yield message

@app.get('/stream')
async def message_stream(request: Request):
    # Connect to nats server
    nc = await nats.connect(NATS_SERVER_URL)

    # Create JetStream context.
    js = nc.jetstream()
    sub = await js.subscribe(FEED_SUBSCRIPTION_SUBJECT, ordered_consumer=True)

    async def event_generator():
        while True:
            # If client closed the connection
            if await request.is_disconnected():
                break

            try:
                async for msg in sub.messages:
                    data = msg.data.decode()
                    print(f"Received a message on '{msg.subject}': {data}")
                    yield {"event": FEED_SUBSCRIPTION_SUBJECT, "data": data}
            except Exception as e:
                print(str(e))

    return EventSourceResponse(event_generator())


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
