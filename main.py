from time import sleep

import uvicorn

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


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level='trace', reload=True)