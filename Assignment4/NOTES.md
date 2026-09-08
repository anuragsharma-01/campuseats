# CS543 Assignment 4 — CampusEats Orders Service

## A1 — Selected service
**Orders Service** is selected. The assignment explicitly allows Catalogue, Orders or Delivery and forbids Payments because Payments was already used in Tutorial 4. This service keeps the Assignment 2 boundary: the Orders service owns order data and does not redesign the service boundaries.

## A2 — SOAP-style starting operations
1. createOrder(...)
2. getOrder(...)
3. listOrders(...)
4. cancelOrder(...)
5. updateOrderStatus(...)

## A3/A4 — Resource table
| Method | URL | What it does | Success code | Failure codes |
|---|---|---|---|---|
| POST | /orders | Creates an order and authorizes payment | 201 | 400, 409, 422, 503 |
| GET | /orders/{orderId} | Reads one order | 200 | 404 |
| GET | /orders?status=confirmed | Filters orders by status | 200 | 400 |
| POST | /orders/{orderId}/cancellation | Requests an order cancellation | 202 | 404, 409, 422 |

## A5 — Hard choice
`cancelOrder(...)` is an action/state transition, so it does not map cleanly to ordinary CRUD. I used `/orders/{orderId}/cancellation` as a state-changing sub-resource. I rejected `/cancelOrder` because verbs should not appear in URLs. I also rejected a broad `PUT /orders/{id}` because it would allow unrelated order fields to be changed.

## C2
The `Order` model stores an internal payment reference, but `as_json()` omits it. Thus the stored record and public representation differ and internal information does not leak.

## C4/C5/C6
`validate()` checks the request before body fields are used. Create returns 201 plus Location; reads return 200; cancellation returns 202; malformed input returns 400; missing orders return 404; state conflicts return 409; valid domain rejection returns 422; dependency failure returns 503. Every failure uses the same `problem()` shape.

## C7/C8
POST /orders requires `Idempotency-Key`. The key is stored with the created order, and repeating the same key returns the original result without creating a second order.

## D1/D2
The Orders Service calls the Payments Service through `PAYMENT_SERVICE_URL`; the URL is never hard-coded. The call has a 2-second timeout, exponential backoff and jitter. 4xx responses are not retried. The retried create carries the same idempotency key.

## D3 — Fallback
If Payments is unreachable, the Orders Service returns 503 and does not create an order in the local store. Degrading to a confirmed order without payment authorization would be unsafe because it could create an order that appears paid when payment was never confirmed.

## Assignment 3 comparison
The supplied Assignment 4 brief asks this section to quote the team's Assignment 3 WSDL/fault. That Assignment 3 artefact was not supplied with this request, so no invented quote is presented here. Replace the marked comparison with the exact line count and exact `soap:Fault` from the team's CampusEats Assignment 3 before submission.

The REST design removes SOAP-specific binding details and represents failures with HTTP status codes plus one common problem body. Returning a failure inside HTTP 200 would mislead intermediaries and clients because 200 means the HTTP operation succeeded.

UDDI's publish/find/bind workflow is no longer required as a live UDDI server. A service catalogue and OpenAPI document can provide discovery and contract information, while HTTP clients bind by using the documented endpoint.

The XML Schema validation responsibility is now carried by `validate()` in `app.py`. Without it, malformed bodies could reach application logic and fail with an uncontrolled server error.

SOAP would still be appropriate for a strict enterprise integration that requires a WSDL contract, SOAP message-level security and standardized SOAP fault handling; that is the guarantee being purchased.

## Team
Anurag Sharma (Leader), Mohit Tailor, Harshita Rathore, Harendra Godara.
TeamID and Roll Numbers were not provided in the supplied material and are therefore left for the team to fill in.
