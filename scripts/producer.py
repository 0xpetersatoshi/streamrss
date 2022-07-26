import asyncio
import os

import nats
from dotenv import load_dotenv

load_dotenv('.env')

NATS_SERVER_URL = os.environ['NATS_SERVER_URL']
FEED_SUBSCRIPTION_SUBJECT = os.environ['FEED_SUBSCRIPTION_SUBJECT']

async def main():
    nc = await nats.connect(NATS_SERVER_URL)

    # Create JetStream context.
    js = nc.jetstream()

    # Persist messages to a subject
    await js.add_stream(name="feed-stream", subjects=[FEED_SUBSCRIPTION_SUBJECT])

    while True:
        import os
        message = os.urandom(10).hex().encode()
        ack = await js.publish(FEED_SUBSCRIPTION_SUBJECT, message)
        print(ack)
        await asyncio.sleep(1)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nshutting producer down and exiting...")
