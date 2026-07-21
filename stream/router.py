from collections.abc import AsyncIterable

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from data import Item, items, message, PNGStreamingResponse, read_image

router = APIRouter(prefix="/stream", tags=["stream"])

@router.get("/items/json-lines")
async def stream_json_items() -> AsyncIterable[Item]:
    """Stream JSON Lines, one JSON object per line."""
    for item in items:
        yield item

@router.get("/story/pure-strings", response_class=StreamingResponse)
async def stream_story() -> AsyncIterable[str]:
    """
    Stream raw text/binary chunks unparsed (ignores return type annotations).

    StreamingResponse requires manual data encoding; FastAPI streams chunks as-is
    without converting them to JSON.
    """
    for line in message:
        yield line

@router.get("/image", response_class=PNGStreamingResponse)
async def stream_image() -> AsyncIterable[bytes]:
    """
    Stream in-memory image bytes.

    Note: Reading from disk/network typically blocks the event loop, but reading
    from an in-memory `io.BytesIO` source here is non-blocking.
    """
    with read_image() as image_file:
        for chunk in image_file:
            yield chunk