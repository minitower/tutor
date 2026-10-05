# Module 4 — API Design: A Contract People and Agents Can Rely On

## Learning objectives
- Design resources, methods, status codes and errors that clients can predict without reading the code
- Make an API safe for retries, double clicks and concurrent edits
- Evolve an API without breaking existing clients

## Lecture outline
1. An API is a product and a contract: frontends, mobile apps, partners and AI agents depend on it, and a published API is hard to change
2. Resources and URLs: nouns, plural collections, sensible nesting; verbs in URLs as an antipattern
3. HTTP methods: safe and idempotent methods, and why it matters for retries
4. Status codes that matter: 200, 201, 204, 400, 401, 403, 404, 409, 422, 429, 5xx
5. One error format for the whole API: Problem Details (RFC 9457)
6. Validation at the boundary; field-level errors
7. Pagination (offset vs cursor), filtering, sorting; naming and data conventions (ISO 8601 with time zone, money in minor units)
8. Idempotency: the `Idempotency-Key` header and how to implement it
9. Concurrent edits: ETag, `If-Match`, optimistic locking
10. Versioning and evolution: additive vs breaking changes, deprecation and the `Sunset` header
11. Auth, scopes and rate limits (`429` + `Retry-After`)
12. Webhooks: signing (HMAC), retries, idempotent receivers
13. REST vs GraphQL vs gRPC vs WebSocket/SSE: when each fits
14. Contract-first: OpenAPI → mock server, generated clients, linting (Spectral), contract tests (Schemathesis)
15. APIs for AI agents: descriptions, examples, predictable errors; why agents make idempotency mandatory

## Lab
Revise the "Slot" OpenAPI from Module 1 and implement the changes: a Problem Details error format, cursor pagination for slots, an `Idempotency-Key` on `POST /bookings`, ETag on booking updates, a signed `booking.created` webhook. Lint the spec with Spectral and run Schemathesis against the running API.
- **With an agent:** ask the agent to review the OpenAPI for inconsistencies (naming, status codes, missing errors), then to write the Schemathesis run; check every finding against the spec yourself.

## Deliverable
Updated `openapi.yaml` passing Spectral, the implementation, a Schemathesis report, and a short ADR on the versioning policy.
