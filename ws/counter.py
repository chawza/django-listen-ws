import asyncio
import json
from redis.asyncio import Redis

import websockets as ws

CURR_COUNTER = 'counter:current'

async def handler(websocket):
    redis = Redis()
    p = redis.pubsub()
    await p.subscribe('counter')
    await redis.set(CURR_COUNTER, 0, nx=True)
    
    curr = await redis.get(CURR_COUNTER)
    await websocket.send(json.dumps({'counter': int(curr)}))

    while True:
        try:
            message = await p.get_message()
            if not message:
                continue

            if message['type'] != 'message':
                continue

            new_counter = message['data']
            await redis.set(CURR_COUNTER, int(new_counter))
            await websocket.send(json.dumps({'counter': int(new_counter)}))
        except ws.ConnectionClosedOK:
            break

async def main():
    async with ws.serve(handler, '', '8001'):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())