import string
import secrets
from queue import Queue, Empty

import uvicorn
import asyncio
from fastapi import Request
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"])

lobbyQueue = Queue()

@app.get("/")
def home():
    return {"Hi!": "Pax!"}

@app.get("/sse")
async def sse(req: Request):
    async def streamFibonacci(num):
        sumBefore, sum = 0, 1
        while sum <= num:
            disconnected = await req.is_disconnected()
            if disconnected:
                break
            yield str(sum)
            sumBefore, sum = sum, sum + sumBefore
            await asyncio.sleep(1)
    return EventSourceResponse(streamFibonacci(10000))

@app.get("/lobby/{room_code}")
async def enterLobby(req: Request, room_code):
    # TODO "validate" the room_code
    async def streamLobbyActivity():
        yield 'Someone entered the lobby.'
        while True:
            disconnected = await req.is_disconnected()
            if disconnected:
                break
            try:
                lobbyActivity = lobbyQueue.get(block=False)
            except Empty:
                pass
            else:
                yield lobbyActivity
    return EventSourceResponse(streamLobbyActivity())

@app.get("/room_request/{room_code}")
async def requestRoom(room_code, name):
    # TODO "validate" the room_code. Only if the room is 
    # joinable do we do these stuff. Otherwise, 4XX
    # TODO We put "Somebody entered the lobby."
    # here even BEFORE they entered the lobby.
    lobbyQueue.put(f"{name} entered the lobby.")
    return room_code

    


@app.post("/room")
async def createRoom():
    # TODO keep track of created rooms.
    alphabet = string.ascii_uppercase + string.digits
    roomCode = ''.join(secrets.choice(alphabet) for i in range(6))
    return roomCode


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level='trace', reload=True)