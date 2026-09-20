import os, uuid, random, time, requests, hashlib, json
from flask import Flask, jsonify, request, make_response
from models import Order, now_iso
from store import OrderStore
from errors import problem, fail

app=Flask(__name__)
store=OrderStore()
STATUS={"pending","confirmed","preparing","ready","delivered","cancelled"}
RATE_LIMIT = 10
RATE_WINDOW = 60
rate_limits = {}
def check_rate_limit():
    client_id = (
        request.headers.get("Authorization")
        or request.remote_addr
        or "unknown"
    )

    now = time.time()

    timestamps = rate_limits.get(client_id, [])

    timestamps = [
        timestamp
        for timestamp in timestamps
        if now - timestamp < RATE_WINDOW
    ]

    if len(timestamps) >= RATE_LIMIT:
        retry_after = max(
            1,
            int(RATE_WINDOW - (now - timestamps[0]))
        )

        response = make_response(
            jsonify(problem(
                429,
                "Too Many Requests",
                "Rate limit exceeded."
            )),
            429
        )

        response.headers["X-RateLimit-Limit"] = str(RATE_LIMIT)
        response.headers["X-RateLimit-Remaining"] = "0"
        response.headers["Retry-After"] = str(retry_after)

        rate_limits[client_id] = timestamps
        return response

    timestamps.append(now)
    rate_limits[client_id] = timestamps

    return None
@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Strict-Transport-Security"] = "max-age=31536000"

    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = (
        "Content-Type, Authorization, Idempotency-Key, "
        "If-None-Match, If-Match, X-HTTP-Method-Override"
    )
    response.headers["Access-Control-Allow-Methods"] = (
        "GET, POST, PUT, PATCH, DELETE, OPTIONS"
    )

    client_id = (
        request.headers.get("Authorization")
        or request.remote_addr
        or "unknown"
    )

    timestamps = rate_limits.get(client_id, [])
    now = time.time()

    timestamps = [
        timestamp
        for timestamp in timestamps
        if now - timestamp < RATE_WINDOW
    ]

    response.headers["X-RateLimit-Limit"] = str(RATE_LIMIT)
    response.headers["X-RateLimit-Remaining"] = str(
        max(0, RATE_LIMIT - len(timestamps))
    )

    return response
PROTECTED_PATHS = {
    "/orders",
}
def make_etag(order):
    payload = json.dumps(
        order.as_json(),
        sort_keys=True,
        separators=(",", ":")
    ).encode("utf-8")
    return '"' + hashlib.sha256(payload).hexdigest() + '"'

def check_content_negotiation():
    if request.method in {"POST", "PUT", "PATCH"}:
        content_type = request.headers.get("Content-Type")

        if content_type and not content_type.startswith("application/json"):
            return fail(problem(
                406,
                "Not Acceptable",
                "Only application/json is supported."
            ))

    accept = request.headers.get("Accept")

    if accept:
        accepted_types = [
            value.strip()
            for value in accept.split(",")
        ]

        if (
            "application/json" not in accepted_types
            and "*/*" not in accepted_types
        ):
            return fail(problem(
                406,
                "Not Acceptable",
                "Only application/json responses are supported."
            ))

    return None
@app.before_request
def require_authorization():
    negotiation_response = check_content_negotiation()
    if negotiation_response:
        return negotiation_response
    limit_response = check_rate_limit()
    if limit_response:
        return limit_response

    if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer ") or not auth[7:].strip():
            return fail(problem(
                401,
                "Unauthorized",
                "Authorization: Bearer <token> is required."
            ))

def validate(body):
    if not isinstance(body,dict):
        return problem(400,"Malformed body","Request body must be a JSON object.")
    for k in ("customer_id","restaurant_id","items"):
        if k not in body:
            return problem(400,"Malformed body",f"Missing required field: {k}")
    if not isinstance(body["customer_id"],str) or not body["customer_id"].strip():
        return problem(400,"Malformed body","customer_id must be a non-empty string.")
    if not isinstance(body["restaurant_id"],str) or not body["restaurant_id"].strip():
        return problem(400,"Malformed body","restaurant_id must be a non-empty string.")
    if not isinstance(body["items"],list) or not body["items"]:
        return problem(422,"Domain validation failed","items must contain at least one item.")
    for item in body["items"]:
        if not isinstance(item,dict) or "menu_item_id" not in item or "quantity" not in item:
            return problem(400,"Malformed body","Each item needs menu_item_id and quantity.")
        if not isinstance(item["quantity"],int) or item["quantity"] < 1:
            return problem(422,"Domain validation failed","quantity must be at least 1.")
    return None

def authorize_payment(order_id, customer_id, idempotency_key):
    url=os.environ.get("PAYMENT_SERVICE_URL")
    if not url:
        raise RuntimeError("PAYMENT_SERVICE_URL is not configured")
    headers={"Content-Type":"application/json","Idempotency-Key":idempotency_key}
    data={"order_id":order_id,"customer_id":customer_id}
    last=None
    for attempt in range(3):
        try:
            r=requests.post(url.rstrip("/")+"/payment-authorizations",
                            json=data,headers=headers,timeout=2)
            if 400 <= r.status_code < 500:
                r.raise_for_status()
            r.raise_for_status()
            return r
        except requests.RequestException as e:
            last=e
            if attempt==2: break
            time.sleep(0.25*(2**attempt)+random.uniform(0,0.15))
    raise RuntimeError(last)

@app.post("/orders")
def create_order():
    body=request.get_json(silent=True)
    p=validate(body)
    if p: return fail(p)
    key=request.headers.get("Idempotency-Key")
    if not key: return fail(problem(400,"Malformed request","Idempotency-Key is required."))
    old=store.existing(key)
    if old:
        o=store.get(old)
        r=make_response(jsonify(o.as_json()),201)
        r.headers["Location"]=f"/orders/{o.id}"
        return r
    order_id=str(uuid.uuid4())
    try:
        authorize_payment(order_id,body["customer_id"],key)
    except requests.HTTPError as e:
        status=e.response.status_code if e.response is not None else 503
        if 400 <= status < 500:
            return fail(problem(422,"Payment refused","Payment could not be authorized."))
        return fail(problem(503,"Service unavailable","Payment service is temporarily unreachable."))
    except Exception:
        return fail(problem(503,"Service unavailable","Payment service is temporarily unreachable."))
    o=Order(order_id,body["customer_id"],body["restaurant_id"],body["items"],
            "confirmed",now_iso(),body.get("delivery_address",""),"internal")
    store.save(o); store.remember(key,o.id)
    r=make_response(jsonify(o.as_json()),201)
    r.headers["Location"]=f"/orders/{o.id}"
    return r

@app.route("/orders", methods=["OPTIONS"])
def options_orders():
    response = make_response("", 204)
    response.headers["Allow"] = "GET, POST, OPTIONS"
    return response
@app.get("/orders")
def list_orders():
    status = request.args.get("status")
    sort = request.args.get("sort", "created_at")
    order = request.args.get("order", "asc")
    page = request.args.get("page", "1")
    limit = request.args.get("limit", "10")

    if status and status not in STATUS:
        return fail(problem(400, "Malformed query", "Unknown order status."))

    if sort not in {"created_at", "status"}:
        return fail(problem(400, "Malformed query", "Invalid sort field."))

    if order not in {"asc", "desc"}:
        return fail(problem(400, "Malformed query", "Invalid sort order."))

    try:
        page = int(page)
        limit = int(limit)
    except ValueError:
        return fail(problem(400, "Malformed query", "page and limit must be integers."))

    if page < 1 or limit < 1 or limit > 100:
        return fail(problem(400, "Malformed query", "page must be >= 1 and limit must be 1-100."))

    orders = store.list(status)

    if sort == "created_at":
        orders = sorted(
            orders,
            key=lambda o: o.created_at,
            reverse=(order == "desc")
        )
    else:
        orders = sorted(
            orders,
            key=lambda o: o.status,
            reverse=(order == "desc")
        )

    start = (page - 1) * limit
    end = start + limit

    selected = orders[start:end]

    return jsonify({
        "items": [o.as_json() for o in selected],
        "page": page,
        "limit": limit,
        "total": len(orders)
    }), 200
@app.route("/orders/<order_id>", methods=["OPTIONS"])
def options_order(order_id):
    response = make_response("", 204)
    response.headers["Allow"] = "GET, PATCH, DELETE, OPTIONS"
    return response
@app.get("/orders/<order_id>")
def get_order(order_id):
    o = store.get(order_id)

    if not o:
        return fail(problem(404, "Not found", "Order does not exist."))

    etag = make_etag(o)

    if request.headers.get("If-None-Match") == etag:
        response = make_response("", 304)
        response.headers["ETag"] = etag
        return response

    response = make_response(jsonify(o.as_json()), 200)
    response.headers["ETag"] = etag
    response.headers["Cache-Control"] = "private, max-age=60"
    return response
@app.patch("/orders/<order_id>")
def update_order(order_id):
    o = store.get(order_id)

    if not o:
        return fail(problem(404, "Not found", "Order does not exist."))

    current_etag = make_etag(o)
    if_match = request.headers.get("If-Match")

    if not if_match:
        return fail(problem(
            412,
            "Precondition failed",
            "If-Match header is required."
        ))

    if if_match != current_etag:
        return fail(problem(
            412,
            "Precondition failed",
            "The resource has changed. Refresh and retry."
        ))

    body = request.get_json(silent=True)

    if not isinstance(body, dict):
        return fail(problem(
            400,
            "Malformed body",
            "Request body must be a JSON object."
        ))

    if "status" not in body or body["status"] not in STATUS:
        return fail(problem(
            422,
            "Domain validation failed",
            "status must be a valid order status."
        ))

    o.status = body["status"]

    new_etag = make_etag(o)

    response = make_response(jsonify(o.as_json()), 200)
    response.headers["ETag"] = new_etag
    return response
@app.delete("/orders/<order_id>")
def delete_order(order_id):
    o = store.get(order_id)

    if not o:
        return fail(problem(
            404,
            "Not found",
            "Order does not exist."
        ))

    del store.orders[order_id]

    return "", 204
@app.post("/orders/<order_id>/cancellation")
def cancel_order(order_id):
    o=store.get(order_id)
    if not o: return fail(problem(404,"Not found","Order does not exist."))
    if o.status=="cancelled": return fail(problem(409,"State conflict","Order is already cancelled."))
    if o.status in {"preparing","ready","delivered"}:
        return fail(problem(409,"State conflict","Order can no longer be cancelled."))
    if o.status=="pending":
        return fail(problem(422,"Domain validation failed","Order is not yet confirmed for cancellation."))
    o.status="cancelled"
    return jsonify(o.as_json()),202

if __name__=="__main__":
    app.run(port=5001)
