---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->
# Module 4
## API Design
### A contract people and agents can rely on

*Modern Application Architecture: From Idea to a Live Product*

---

<!-- Slide 2 -->
## Session plan

- The API as a product and a contract
- Resources, URLs, methods, status codes
- One error format and validation
- Pagination, filters, data conventions
- Idempotency and concurrent edits
- Versioning and evolving an API
- Auth, rate limits, webhooks
- REST, GraphQL, gRPC — which when
- Contract-first and APIs for AI agents
- Lab

---

<!-- Slide 3 -->
## Learning objectives

- Design an API whose behavior a client can **predict** without reading the code
- Make an API safe for retries, double clicks and concurrent edits
- Evolve an API **without breaking** existing clients
- Describe the contract in OpenAPI and check the implementation automatically

---

<!-- Slide 4 -->
## An API is a product and a contract

- API clients: your frontend, a mobile app, partners, **AI agents**
- Internal code can be rewritten in an evening; a published API can't — old app versions live on users' phones for years
- A good API is **boring and predictable**: see one endpoint and you can guess the rest
- Every decision here is for people and for agents that read the OpenAPI and call the API without you

---

<!-- Slide 5 -->
## Resources and URLs

| Bad | Good |
|---|---|
| `POST /createBooking` | `POST /api/bookings` |
| `GET /getSlotsForMaster?id=7` | `GET /api/masters/7/slots` |
| `POST /api/bookings/1017/cancel` | `PATCH /api/bookings/1017` with `{"status": "cancelled"}` — or an explicit action if it's a separate business process |
| `GET /api/Booking_List` | `GET /api/bookings` |

- URLs are **nouns**, collections are plural
- One nesting level at most: `/masters/7/slots`, not `/masters/7/services/3/slots/42/bookings`
- The action is the HTTP method, not a verb in the path

---

<!-- Slide 6 -->
## Methods: safe and idempotent

| Method | What it does | Safe | Idempotent |
|---|---|---|---|
| `GET` | Read | Yes | Yes |
| `PUT` | Replace entirely | No | Yes |
| `DELETE` | Delete | No | Yes |
| `PATCH` | Change part | No | Not necessarily |
| `POST` | Create / action | No | **No** |

- **Safe** — changes nothing on the server
- **Idempotent** — repeating the request has the same effect as sending it once
- The network is unreliable: clients, proxies and SDKs **retry**. A retried `POST` is a second booking.

---

<!-- Slide 7 -->
## The status codes you actually need

| Code | When |
|---|---|
| `200 OK` / `201 Created` / `204 No Content` | Success: read / created / deleted |
| `400 Bad Request` | The request can't be parsed |
| `401 Unauthorized` | We don't know who you are |
| `403 Forbidden` | We know, but you can't |
| `404 Not Found` | No such resource (or you may not know it exists) |
| `409 Conflict` | A state conflict: the slot is already taken |
| `422 Unprocessable Content` | The data failed validation |
| `429 Too Many Requests` | Rate limit exceeded |
| `500` / `503` | Server error / temporarily unavailable |

Rule: `4xx` — the client can fix the request; `5xx` — not the client's fault, retry later.

---

<!-- Slide 8 -->
## One error format: Problem Details (RFC 9457)

```
HTTP/1.1 409 Conflict
Content-Type: application/problem+json

{
  "type": "https://slot.example/errors/slot-taken",
  "title": "Slot already taken",
  "status": 409,
  "detail": "Slot 42 was booked at 14:03",
  "instance": "/api/bookings",
  "nearest_free_slots": [43, 47]
}
```

- One format for the whole API — the frontend and an agent parse errors with one piece of code
- `type` is a stable identifier the client uses to decide what to do
- Extra members (`nearest_free_slots`) are allowed by the standard

---

<!-- Slide 9 -->
## Validation at the boundary

```
HTTP/1.1 422 Unprocessable Content
Content-Type: application/problem+json

{
  "type": "https://slot.example/errors/validation",
  "title": "Validation failed",
  "status": 422,
  "errors": [
    {"field": "phone", "message": "Expected a number like +7XXXXXXXXXX"},
    {"field": "slot_id", "message": "The slot is in the past"}
  ]
}
```

- Validate **everything** that comes from the client: types, formats, ranges, permissions
- Errors **per field**, so the form highlights the right place
- Pydantic / FastAPI do basic validation from types; business rules are your code

---

<!-- Slide 10 -->
## Pagination

| | Offset: `?page=3&size=20` | Cursor: `?cursor=…&limit=20` |
|---|---|---|
| How it works | Skip N rows | Continue after the last item |
| Jump to page 50 | Possible | Not possible |
| New rows while paging | Duplicates and gaps | Stable |
| Speed on large tables | Degrades: the DB still reads N rows | Constant (via an index) |

```json
{ "items": [ ... ], "next_cursor": "eyJzdGFydHNfYXQiOiIyMDI2LTEwLTA5VDE1OjAwIiwiaWQiOjQ3fQ" }
```

The cursor is an opaque string to the client (it encodes the last item's key). Lists always have a limit.

---

<!-- Slide 11 -->
## Filters, sorting, data conventions

- Filters and sorting as parameters: `GET /api/slots?master_id=7&from=2026-10-09&sort=starts_at`
- One naming style across the API: `snake_case` **or** `camelCase`, never mixed
- Dates and times — **ISO 8601 with a time zone**: `2026-10-09T15:00:00+03:00`
- Money — **an integer in minor units** + currency: `{"amount": 90000, "currency": "RUB"}` = 900 ₽
- IDs — strings or numbers, but the same everywhere
- `null` vs a missing field — agree on what each means

---

<!-- Slide 12 -->
## Idempotency: the problem

The client clicks "Book" → the request arrives, the booking is created → the response is lost (bad network) → the client or SDK **retries**.

Without protection — **two bookings**, or, if the first request already took the slot, the client sees "Slot taken" for their own booking.

The fix is an **idempotency key**:

```
POST /api/bookings
Idempotency-Key: 9b2f6c1e-4d7a-4f0e-9a51-3c8e2b7d1a44
```

The client generates the key (a UUID) **once per action** and reuses it on retries. On a repeat with the same key the server returns the **stored** response.

---

<!-- Slide 13 -->
## Idempotency: the implementation

```python
@app.post("/api/bookings", status_code=201)
async def create_booking(data: BookingCreate, idempotency_key: str = Header()):
    saved = await repo.get_idempotent(idempotency_key)
    if saved:
        if saved.request_hash != hash_of(data):
            raise HTTPException(422, "Key already used with a different body")
        return saved.response                     # a retry: the same response
    booking = await book_slot(data)
    await repo.save_idempotent(idempotency_key, hash_of(data), booking)
    return booking
```

- The key is stored **in the same transaction** as the booking, with a unique index — two concurrent retries can't both succeed
- Keys are kept for a limited time (e.g. 24 hours)
- The same key with a **different** body is a client error

---

<!-- Slide 14 -->
## Concurrent edits: ETag and If-Match

The barber and an admin edit the same booking at once — the last one wins, the first one's change is silently lost.

```
GET /api/bookings/1017          →  200, ETag: "v7"
PATCH /api/bookings/1017
If-Match: "v7"                  →  200, ETag: "v8"
PATCH /api/bookings/1017
If-Match: "v7"                  →  412 Precondition Failed (already changed)
```

- This is **optimistic locking**: no lock is held, the version is checked on write
- Inside — a `version` column: `UPDATE ... SET version = version + 1 WHERE id = 1017 AND version = 7`

---

<!-- Slide 15 -->
## Versioning and evolution

**Safe to add** (doesn't break clients):
- new endpoints, new optional request fields, new response fields

**Breaking changes** (need a new version):
- removing or renaming a field, changing a type, making a field required, changing what a status code means

Options: in the path `/api/v1/...` (simplest), in a header, by version date.

Retiring a version: announce it early, send `Deprecation` and `Sunset` headers, watch the logs for who still calls the old version.

---

<!-- Slide 16 -->
## Auth and rate limits

- Users — a session or a token; partners — **API keys** with scopes: `bookings:read`, `bookings:write`
- Permissions are checked on **every** request, on the server — not just "is someone logged in" but "is this their booking"
- **Rate limits** protect against brute force and runaway loops:

```
HTTP/1.1 429 Too Many Requests
Retry-After: 30
```

- Limits per user, key, IP; stricter on expensive operations (booking, LLM calls)

---

<!-- Slide 17 -->
## Webhooks: the API in reverse

The server tells a partner about an event itself: "booking created" → POST to the partner's URL.

```python
import hashlib, hmac

def verify(body: bytes, timestamp: str, signature: str, secret: bytes) -> bool:
    signed = timestamp.encode() + b"." + body
    expected = hmac.new(secret, signed, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)
```

- **Signature** (HMAC) — the receiver checks the webhook came from you; the timestamp protects against replaying old messages
- **Retries** with growing backoff if the receiver doesn't answer `2xx`
- The receiver is **idempotent**: one event may arrive twice — store the `event_id`

---

<!-- Slide 18 -->
## REST, GraphQL, gRPC, WebSocket / SSE

| | Strength | When |
|---|---|---|
| **REST** | Simple, cacheable, understood by everyone | The default, public APIs |
| **GraphQL** | The client picks the fields, one request instead of five | Complex frontends, lots of related data, many client types |
| **gRPC** | Binary, fast, strict schema, streaming | Service-to-service calls inside a system |
| **WebSocket / SSE** | The server pushes updates | Chats, live statuses, streaming LLM answers (Module 7) |

For "Slot": REST outside. SSE for live free-slot updates.

---

<!-- Slide 19 -->
## Contract-first: OpenAPI as the source of truth

1. Change `openapi.yaml` first, review it in a PR
2. **Spectral** — a spec linter: naming, status codes, descriptions
3. **Prism** — a mock server for the frontend before the backend is ready
4. **Generated clients** — a typed client for the frontend instead of hand-written `fetch`
5. **Schemathesis** — generates thousands of requests from the spec and finds where the implementation disagrees

If the contract and the code disagree, the contract lies — and every client copies the lie.

---

<!-- Slide 20 -->
## APIs for AI agents

- An agent reads OpenAPI **descriptions** literally: say what an endpoint does and when to call it
- **Examples** of requests and responses in the spec are the best hint
- **Predictable errors**: from `type` and `detail` the agent knows what to fix
- Agents **retry** more than people → idempotency is mandatory
- Dangerous actions get their own endpoints with their own permissions
- An **MCP server** on top of the API is easy — and "Slot" becomes a tool for any agent

---

<!-- Slide 21 -->
## Lab

1. Revise the "Slot" OpenAPI: Problem Details errors, cursor pagination for slots, `Idempotency-Key` on `POST /bookings`, ETag on booking updates
2. Implement the changes in the API
3. A signed `booking.created` webhook and a receiver that verifies the signature
4. Lint the spec with **Spectral**, run **Schemathesis** against the running API
5. **With an agent:** ask the agent to find inconsistencies in the OpenAPI (naming, codes, missing errors) and write the Schemathesis run; check every finding against the spec yourself

---

<!-- Slide 22 -->
## Deliverable

- An `openapi.yaml` that passes Spectral
- The implementation: errors, pagination, idempotency, ETag, webhook
- The Schemathesis report and what you fixed
- An ADR on the versioning policy

---

<!-- Slide 23 -->
## Recap and next module

- An API is a contract: predictable URLs, methods, codes and errors
- The network retries → idempotency and ETags
- Adding is fine, breaking only with a new version
- Contract first, the implementation is checked against it automatically
- Next: **Module 5 — Databases**: the data model, transactions, and making double booking impossible
