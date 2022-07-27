import asyncio
import json
import os

import nats
from dotenv import load_dotenv
from streamrss.feeds.feed_handler import FeedHandler


BASE_DIR= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, '.env'))

# TODO: use env vars instead of hardcoding
NATS_SERVER_URL = "nats://localhost:4222"
FEED_SUBSCRIPTION_SUBJECT = 'feed.events'


async def main(state: dict):
    nc = await nats.connect(NATS_SERVER_URL)

    # Create JetStream context.
    js = nc.jetstream()

    # Persist messages to a subject
    await js.add_stream(name="feed-stream", subjects=[FEED_SUBSCRIPTION_SUBJECT])

    print(f"initial state: {state}")
    while True:
        feed_handler = FeedHandler(state)
        for row in feed_handler.get_feeds():
            encoded_row = json.dumps(row).encode()
            ack = await js.publish(FEED_SUBSCRIPTION_SUBJECT, encoded_row)
            print(ack)

        # Update the state
        state = feed_handler.get_state()

        # Sleep for 30 seconds before re-fetching all the feeds
        print("sleeping for 30 seconds...")
        await asyncio.sleep(30)


if __name__ == '__main__':
    state = {"start_date": "2022-07-01"}
    try:
        asyncio.run(main(state))
    except KeyboardInterrupt:
        print("\nshutting producer down and exiting...")
