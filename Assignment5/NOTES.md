# CS543 Assignment 5 — CampusEats Orders Service

## Team

* Anurag Sharma (Leader)
* Mohit Tailor
* Harshita Rathore
* Harendra Godara
* TeamID: `<FILL TEAM ID>`
* Roll Numbers: `<FILL ROLL NUMBERS>`

---

# Part A — REST Resource and HTTP Method Design

## A1 — Selected service

**Orders Service** is selected. The service keeps the existing CampusEats boundary: the Orders Service owns order data and does not redesign the service boundaries.

## A2 — Original SOAP-style operations

1. `createOrder(...)`
2. `getOrder(...)`
3. `listOrders(...)`
4. `cancelOrder(...)`
5. `updateOrderStatus(...)`

## A3/A4 — REST resource and method map

| Method | URL                              | Purpose                          | Success | Important failures           |
| ------ | -------------------------------- | -------------------------------- | ------- | ---------------------------- |
| POST   | `/orders`                        | Create an order                  | 201     | 400, 401, 422, 429, 503      |
| GET    | `/orders`                        | List/filter/sort/paginate orders | 200     | 400, 429                     |
| GET    | `/orders/{orderId}`              | Read one order                   | 200     | 404, 429                     |
| PATCH  | `/orders/{orderId}`              | Update order status              | 200     | 400, 401, 404, 412, 422, 429 |
| DELETE | `/orders/{orderId}`              | Delete an order                  | 204     | 401, 404, 429                |
| POST   | `/orders/{orderId}/cancellation` | Request cancellation             | 202     | 401, 404, 409, 422, 429      |

## A5 — Hard choice: cancellation

`cancelOrder(...)` is an action/state transition, so it does not map cleanly to ordinary CRUD.

The REST design therefore uses:

`POST /orders/{orderId}/cancellation`

This represents creation of a cancellation action/sub-resource rather than putting a verb such as `/cancelOrder` into the URL.

A broad `PUT /orders/{id}` was not used for cancellation because it could imply replacement or modification of unrelated order fields.

## Safe and idempotent methods

* `GET` is safe and idempotent.
* `OPTIONS` is safe and idempotent.
* `POST /orders` is not inherently idempotent, but `Idempotency-Key` makes retries safe for the same logical create request.
* `POST /orders/{orderId}/cancellation` changes state and is therefore not treated as a safe method.
* `PATCH /orders/{orderId}` changes resource state and requires `If-Match`.
* `DELETE /orders/{orderId}` is not safe, although repeating deletion of an already deleted resource does not create another deletion.

## OPTIONS

The service exposes `OPTIONS` responses with an `Allow` header.

For `/orders`:

`Allow: GET, POST, OPTIONS`

For `/orders/{orderId}`:

`Allow: GET, PATCH, DELETE, OPTIONS`

CORS preflight response headers are also returned.

## Query filtering, sorting and pagination

`GET /orders` supports:

* `status`
* `sort`
* `order`
* `page`
* `limit`

Example:

`GET /orders?status=confirmed&sort=created_at&order=desc&page=1&limit=10`

Invalid query values return `400`.

---

# Part B — HTTP Semantics and Security

## JSON representation

The API uses JSON representations for request and response bodies.

The OpenAPI contract documents `application/json` request bodies.

## Status code conventions

* `201 Created` — successful order creation.
* `200 OK` — successful reads and updates.
* `202 Accepted` — cancellation request accepted.
* `204 No Content` — successful deletion and OPTIONS responses.
* `304 Not Modified` — conditional GET when the supplied ETag matches.
* `400 Bad Request` — malformed request/query data.
* `401 Unauthorized` — missing or invalid Bearer authorization.
* `404 Not Found` — requested order does not exist.
* `409 Conflict` — invalid state transition such as cancelling an order that can no longer be cancelled.
* `412 Precondition Failed` — failed `If-Match` condition.
* `422 Unprocessable Entity` — valid JSON but invalid domain data.
* `429 Too Many Requests` — rate limit exceeded.
* `503 Service Unavailable` — payment dependency unavailable.

## Authorization

State-changing methods require:

`Authorization: Bearer <token>`

Missing authorization returns `401 Unauthorized`.

GET requests remain readable without this state-changing authorization requirement.

## Cache validation

Individual order responses include:

`ETag: "<etag-value>"`

and:

`Cache-Control: private, max-age=60`

When the client sends a matching `If-None-Match`, the service returns:

`304 Not Modified`

with the matching ETag.

## Conditional writes

PATCH requests require `If-Match`.

If the supplied ETag is stale or does not match the current representation, the service returns:

`412 Precondition Failed`

This prevents an update from silently overwriting a newer representation.

## Rate limiting

The service uses a configured limit of 10 requests per 60-second window.

Responses include:

* `X-RateLimit-Limit`
* `X-RateLimit-Remaining`

When the limit is exceeded, the service returns:

`429 Too Many Requests`

and includes:

`Retry-After`

## CORS

The service returns CORS headers including:

* `Access-Control-Allow-Origin: *`
* `Access-Control-Allow-Headers`
* `Access-Control-Allow-Methods`

OPTIONS responses therefore also support browser preflight requests.

## Security headers

Responses include:

`X-Content-Type-Options: nosniff`

and:

`Strict-Transport-Security: max-age=31536000`

---

# Part C — Idempotency and Conditional Requests

## Idempotency-Key

`POST /orders` requires an `Idempotency-Key`.

The key is stored with the created order.

If the same key is submitted again, the existing order is returned instead of creating another order.

The successful create response is:

`201 Created`

with a `Location` header pointing to the created order.

The payment authorization request also carries the same idempotency key when contacting the payment service.

## Conditional GET

The client first performs:

`GET /orders/{orderId}`

The response provides an ETag.

The client can then send:

`If-None-Match: "<etag>"`

If the representation has not changed, the service returns:

`304 Not Modified`

## Conditional update

The client sends:

`If-Match: "<current-etag>"`

with the PATCH request.

If the representation has changed since the client obtained the ETag, the request fails with:

`412 Precondition Failed`

The client must GET the current representation, obtain the new ETag, re-apply its intended change, and retry the PATCH with the new ETag.

## Safe retry plan

| Operation         | Retry approach                                       |
| ----------------- | ---------------------------------------------------- |
| GET order         | Safe to retry                                        |
| GET order list    | Safe to retry                                        |
| POST create       | Retry using the same `Idempotency-Key`               |
| PATCH update      | Re-fetch current ETag before retrying after `412`    |
| DELETE            | Retry only after checking the current resource state |
| Cancellation POST | Retry carefully and check current order state        |

---

# Part D — Evidence and HTTP Exchanges

The `curl-transcript.txt` file contains the required HTTP examples for:

1. `201 Created` plus `Location`
2. Repeated create with the same idempotency key
3. Conditional GET returning `304`
4. Conditional write returning `412`
5. Malformed request returning `400`
6. Missing resource returning `404`
7. Missing authorization returning `401`
8. OPTIONS and `Allow`
9. Rate limiting and `429`

The transcript uses `curl.exe` so that it invokes curl directly from PowerShell rather than the PowerShell `curl` alias.

---

# Existing Assignment 4 Design Decisions

## C2 — Internal payment reference

The `Order` model stores an internal payment reference, but `as_json()` omits it. Therefore the stored record and public representation differ and internal information is not exposed through the API.

## Payment dependency

The Orders Service calls the Payments Service using the `PAYMENT_SERVICE_URL` environment variable; the URL is not hard-coded.

The payment request uses:

* a 2-second timeout
* exponential backoff
* jitter
* the same `Idempotency-Key` across retries

4xx payment responses are not retried.

## Dependency failure

If the Payments Service is unreachable, the Orders Service returns `503 Service Unavailable` and does not create the order in the local store.

Creating a confirmed order without successful payment authorization would allow the local order state to claim confirmation when payment had not been confirmed.

## Validation and common errors

`validate()` checks required fields and data types before the order is created.

Failure responses use the common `problem()` structure.

---

# Assignment 3 comparison

The supplied Assignment 3 WSDL/fault artefact is not available in the current material, so an exact quotation should not be invented.

The REST design replaces SOAP-specific binding details with HTTP methods, resource URLs, HTTP status codes, headers and JSON representations.

SOAP-style faults are represented through appropriate HTTP status codes and the common problem response structure.

UDDI-style publish/find/bind discovery is replaced by the documented service endpoint and OpenAPI contract.

The XML Schema validation responsibility is implemented through request validation in `app.py`.

SOAP may still be appropriate where an integration specifically requires WSDL contracts, SOAP message-level security and standardized SOAP fault handling.

---

# Submission checklist

Before submission, verify:

* [ ] `app.py` updated
* [ ] `test_app.py` passes
* [ ] `openapi.yaml` is present and valid
* [ ] `curl-transcript.txt` contains required exchanges
* [ ] `NOTES.md` contains TeamID and roll numbers
* [ ] All source files are included
* [ ] Tests pass with `pytest -q`
* [ ] Git changes are committed
* [ ] Changes are pushed to the same repository
* [ ] Team Leader prepares the final ZIP
