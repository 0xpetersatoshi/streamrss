import asyncio
import json
import os

import nats
from dotenv import load_dotenv
from streamrss.feeds.blockworks import Blockworks
from streamrss.feeds.decrypt import Decrypt

BASE_DIR= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, '.env'))

NATS_SERVER_URL = "nats://localhost:4222"
FEED_SUBSCRIPTION_SUBJECT = 'feed.events'

async def main():
    nc = await nats.connect(NATS_SERVER_URL)

    # Create JetStream context.
    js = nc.jetstream()

    # Persist messages to a subject
    await js.add_stream(name="feed-stream", subjects=[FEED_SUBSCRIPTION_SUBJECT])

    while True:
        for row in get_feeds():
            encoded_row = json.dumps(row).encode()
            ack = await js.publish(FEED_SUBSCRIPTION_SUBJECT, encoded_row)
            print(ack)
            await asyncio.sleep(1)

FEEDS = {
    "blockworks": Blockworks,
    "decrypt": Decrypt
}

def get_feeds():
    for feed in FEEDS:
        f = FEEDS[feed]()
        yield from f.get_entries()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nshutting producer down and exiting...")
