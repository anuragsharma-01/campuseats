# CampusEats —  Assignment 6

## Orders Service

**Selected Service:** CampusEats Orders Service

### Team

- Anurag Sharma — Leader
- Mohit Tailor
- Harshita Rathore
- Harendra Godara


## 1. Project Overview

CampusEats Orders Service is a RESTful web service developed using Python and Flask. Assignment 6 focuses on improving HTTP responses, request validation, and error handling.

The main objective is to return appropriate HTTP status codes and consistent error responses for successful and unsuccessful requests.

## 2. Objectives

- Implement appropriate HTTP status codes.
- Return errors using the Problem Details format.
- Validate incoming order data.
- Handle unsupported request and response media types.
- Support idempotency keys for order creation.
- Handle payment failures and service unavailability.
- Document API endpoints using OpenAPI.
- Test API behaviour using automated tests and curl.

## 3. Technologies Used

- Python
- Flask
- Pytest
- JSON
- OpenAPI
- curl

## 4. Main Features

### 4.1 HTTP Status Codes

The service uses appropriate HTTP status codes, including:

- 200 OK – Request completed successfully.
- 201 Created – Order created successfully.
- 400 Bad Request – Invalid request data.
- 401 Unauthorized – Authentication is missing or invalid.
- 404 Not Found – Requested resource does not exist.
- 406 Not Acceptable – Requested response format is unsupported.
- 409 Conflict – Request conflicts with the current resource state.
- 412 Precondition Failed – Request precondition was not satisfied.
- 422 Unprocessable Content – Request cannot be processed due to a validation or business error.
- 429 Too Many Requests – Rate limit exceeded.
- 503 Service Unavailable – Required service is temporarily unavailable.

### 4.2 Problem Details

Error responses use a structured JSON format with fields such as:

- `type` – Identifies the error category.
- `title` – Short error description.
- `status` – HTTP status code.
- `detail` – Explanation of the error.

### 4.3 Request Validation

The API validates incoming order data before processing an order. Missing or invalid required fields should result in an appropriate error response.

### 4.4 Content Negotiation

The service checks the request Content-Type and the client's Accept header. Unsupported media types are rejected with an appropriate error response.

### 4.5 Idempotency

The order creation endpoint uses an `Idempotency-Key` to help prevent duplicate order creation when a client retries a request.

### 4.6 Payment Error Handling

Payment failures and temporary payment-service failures are handled separately using appropriate error responses.

## 5. Project Structure

```text
Assignment6/
├── app.py
├── errors.py
├── models.py
├── store.py
├── openapi.yaml
├── test_app.py
├── requirements.txt
├── NOTES.md
├── VALIDATION_OUTPUT.txt
├── curl-transcript.txt
└── README.md
```

## 6. Installation and Setup

Open a terminal in the Assignment6 directory and install the required dependencies:

```bash
pip install -r requirements.txt
```

## 7. Run the Application

Start the Flask application:

```bash
python app.py
```

The service runs locally at:

```text
http://127.0.0.1:5001
```

## 8. Run Automated Tests

Run the test suite using:

```bash
python -m pytest -q
```

The recorded test run completed with 8 passed tests.

## 9. API Testing

Example: retrieve the orders list.

```bash
curl.exe -i http://127.0.0.1:5001/orders -H "Accept: application/json"
```

Example: request an unsupported response format.

```bash
curl.exe -i http://127.0.0.1:5001/orders -H "Accept: application/xml"
```

The second request demonstrates the handling of an unsupported response format.

Additional request and response examples are available in `curl-transcript.txt` and `VALIDATION_OUTPUT.txt`.

## 10. API Documentation

The `openapi.yaml` file documents the Orders Service API, including endpoints, request parameters, and responses.

The `NOTES.md` file contains additional implementation and design notes.

## 11. Conclusion

Assignment 6 improves the CampusEats Orders Service by focusing on HTTP status codes, structured error responses, request validation, content negotiation, and idempotency. These improvements make API behaviour clearer and help clients handle errors consistently.
