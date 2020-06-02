import uvicorn
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"])


async def streamFibonacci(num):
    sumBefore, sum = 0, 1
    while sum <= num:
        yield f'data: {str(sum)}\n\n'
        sumBefore, sum = sum, sum + sumBefore
        await asyncio.sleep(1)


@app.get("/")
def home():
    return {"Hi!": "Pax!"}

@app.get("/sse")
async def sse():
    fibonacciGenerator = streamFibonacci(10000)
    return EventSourceResponse(fibonacciGenerator)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level='trace', reload=True)