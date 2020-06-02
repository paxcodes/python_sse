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
            yield f'data: {str(sum)}\n\n'
            sumBefore, sum = sum, sum + sumBefore
            await asyncio.sleep(1)
    return EventSourceResponse(streamFibonacci(10000))

@app.post("/room")
async def createRoom():
    alphabet = string.ascii_uppercase + string.digits
    roomCode = ''.join(secrets.choice(alphabet) for i in range(6))
    return roomCode


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level='trace', reload=True)