# CampusEats — Tutorial 5 / Assignment 5

## Orders Service

**Selected Service:** CampusEats Orders Service

### Team

- Anurag Sharma — Leader
- Mohit Tailor
- Harshita Rathore
- Harendra Godara

### Submission Files

- `openapi.yaml`
- `app.py`
- `models.py`
- `store.py`
- `errors.py`
- `tests/test_app.py`
- `NOTES.md`
- `curl-transcript.txt`
- `VALIDATION_OUTPUT.txt`
- `requirements.txt`

### REST Flow

CampusEats Client
      ↓
Orders Service
      ↓
Order Validation
      ↓
Payment Authorization
      ↓
Order Store
      ↓
JSON Response

### HTTP

`GET /orders`

`POST /orders`

`GET /orders/{orderId}`

`PATCH /orders/{orderId}`

`DELETE /orders/{orderId}`

`POST /orders/{orderId}/cancellation`

### API Features

- Bearer authentication
- JSON content negotiation
- Request validation
- Idempotency for order creation
- Payment authorization with retry
- Filtering, sorting and pagination
- ETag and conditional GET
- `If-Match` concurrency control
- Order cancellation
- Rate limiting
- CORS and security headers
- Structured error responses
- OpenAPI documentation

### Run

```bash
pip install -r requirements.txt
export PAYMENT_SERVICE_URL=http://localhost:6000
python app.py
