# FastAPI Notes

I am learning FastAPI here. Below are my concepts and notes.

---

## Code References

- **Streaming & Raw Data:** [stream/router.py](stream/router.py)
- **Server-Sent Events (SSE):** [sse/router.py](sse/router.py)
- **Data Models & Helpers:** [data.py](data.py)
- **App Entry Point:** [main.py](main.py)

---

## Concepts Index

- [Stream JSON Lines](#stream-json-lines)
- [Stream Raw & Binary Data](#stream-raw--binary-data)
- [Server-Sent Events (SSE)](#server-sent-events-sse)

---

## Streaming

### Stream JSON Lines

- **Concept:** Stream items one-by-one as they become ready without waiting for the full collection or wrapping in a JSON array `[...]`.
- **Content-Type:** `application/jsonl`
- **Format:** One valid JSON object per line, separated by a newline (`\n`).
- **FastAPI Mechanism:** Return `AsyncIterable[Item]`. FastAPI automatically serializes each yielded Pydantic model or dictionary into a JSON line.

### Stream Raw & Binary Data

- **Concept:** Stream raw unparsed text (e.g., live LLM output chunks) or binary streams (e.g., images, files) chunk-by-chunk.
- **Response Class:** Use `StreamingResponse`.
- **Key Behaviors:**
  - **Bypasses JSON:** FastAPI streams yielded strings/bytes directly without Pydantic validation or JSON conversion.
  - **Type Annotations:** `AsyncIterable[str]` or `AsyncIterable[bytes]` serve as editor hints only; FastAPI does not enforce them at runtime.
  - **Custom Media Types:** Create a custom subclass of `StreamingResponse` (e.g., `PNGStreamingResponse`) to define the `media_type` header (e.g., `image/png`).

### Server-Sent Events (SSE)

- **Concept:** Standardized real-time server-to-client streaming over HTTP. Supported natively by browsers (`EventSource` API) and protocols like MCP.
- **Content-Type:** `text/event-stream`
- **Response Class:** Use `EventSourceResponse` from `fastapi.sse`.
- **Key Behaviors:**
  - **Event Structure:** Messages are formatted with fields like `data:`, `event:`, `id:`, and `retry:`, separated by blank lines.
  - **Plain Data:** Yielding objects directly places them in the `data:` field as JSON.
  - **Explicit Events:** Yield `ServerSentEvent` objects to set custom event names, IDs, comments, or retry intervals.
  - **Raw Data:** Use `raw_data` field when sending non-JSON payload strings.
  - **Connection Resuming:** When disconnected, clients send the `Last-Event-ID` header upon reconnecting so the server can resume from where it left off.
  - **HTTP Methods:** Works with any HTTP method (GET, POST, etc.).