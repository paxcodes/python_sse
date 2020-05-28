from time import sleep

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"])


def streamFibonacci(num):
    sumBefore, sum = 0, 1
    while True:
        yield f'data: {str(sum)}\n\n'
        sumBefore, sum = sum, sum + sumBefore
        sleep(1)

@app.get("/")
def home():
    return {"Hi!": "Pax!"}

@app.get("/sse")
def sse():
    return StreamingResponse(streamFibonacci(500), media_type="text/event-stream")
