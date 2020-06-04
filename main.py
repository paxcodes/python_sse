import string
import secrets

import uvicorn
import asyncio
from fastapi import Request
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"])


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
    return EventSourceResponse(streamLobbyActivity())

@app.post("/room")
async def createRoom():
    # TODO keep track of created rooms.
    alphabet = string.ascii_uppercase + string.digits
    roomCode = ''.join(secrets.choice(alphabet) for i in range(6))
    return roomCode


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level='trace', reload=True)