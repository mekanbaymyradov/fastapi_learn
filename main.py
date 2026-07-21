from fastapi import FastAPI

from stream.router import router as stream_router
from sse.router import router as sse_router


app = FastAPI()


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}


app.include_router(stream_router)
app.include_router(sse_router)