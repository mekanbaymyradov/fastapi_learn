from collections.abc import AsyncIterable

from fastapi import APIRouter, Header
from fastapi.sse import EventSourceResponse, ServerSentEvent
from typing import Annotated

from data import Item, items

router = APIRouter(prefix="/sse", tags=["sse"])


@router.get("/items", response_class=EventSourceResponse)
async def sse_items() -> AsyncIterable[Item]:
    """Each yielded item is encoded as JSON and sent in the "data:" field of an SSE event."""
    for item in items:
        yield item

@router.get("/items/with-server-sent-event-object", response_class=EventSourceResponse)
async def sse_items_with_server_sent_event_object() -> AsyncIterable[ServerSentEvent]:
    """
    ServerSentEvent object has fields like event, id, retry, or comment, 
    you can yield ServerSentEvent objects instead of plain data.
    """
    for i, item in enumerate(items):
        yield ServerSentEvent(data=item, event="item_update", id=str(i+1))

@router.get("/items/with-last-event-id-header", response_class=EventSourceResponse)
async def sse_items_with_last_event_id_header(
    last_event_id: Annotated[int | None, Header()] = None
) -> AsyncIterable[ServerSentEvent]:
    """
    The last event ID is sent in the "Last-Event-ID" header, allowing the client to resume from that point.
    """
    start = last_event_id if last_event_id is not None else 0
    for i, item in enumerate(items[start:], start=start):
        yield ServerSentEvent(data=item, event="item_update", id=str(i+1))
