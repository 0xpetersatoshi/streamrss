import json
import os
import re
import uuid

import nats
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
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
    rules = db.session.query(models.Rules).all()
    return {"rules": rules}

@app.delete('/stream/rules/{rule_id}')
async def rule(rule_id: int):
    rule = db.session.get(models.Rules, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="rule not found")
    db.session.delete(rule)
    db.session.commit()
    return {"ok": True}

@app.get('/stream')
async def message_stream(request: Request):
    # Get list of rules to filter records for
    rules = db.session.query(models.Rules).all()
    rules_exist = True if len(rules) > 0 else False

    # Connect to nats server
    nc = await nats.connect(NATS_SERVER_URL)

    # Create JetStream context.
    js = nc.jetstream()
    print(f"subscribing to stream: {FEED_SUBSCRIPTION_SUBJECT}")
    sub = await js.subscribe(FEED_SUBSCRIPTION_SUBJECT, ordered_consumer=True)

    async def event_generator():
        while True:
            # If client closed the connection
            if await request.is_disconnected():
                break

            try:
                # Loop through messages in jetsream
                async for msg in sub.messages:
                    data = msg.data.decode()
                    print(f"Received a message on '{msg.subject}': {data}")
                    # Loop through the rules and use regex to see if record matches a rule
                    # If there is a match, emit the event

                    if rules_exist:
                        # TODO: figure out why this logic is not working
                        for rule in rules:
                            content = json.loads(data)["content"]
                            m = re.search(rule["pattern"], content)
                            if m:
                                event_id = f"{FEED_SUBSCRIPTION_SUBJECT}::{uuid.uuid4().hex}"
                                yield {"id": event_id, "event": rule["tag"], "data": data}
                    else:
                        yield {"id": uuid.uuid4().hex, "event": FEED_SUBSCRIPTION_SUBJECT, "data": data}
            except Exception as e:
                print(str(e))

    return EventSourceResponse(event_generator())


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
