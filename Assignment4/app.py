import os, uuid, random, time, requests
from flask import Flask, jsonify, request, make_response
from models import Order, now_iso
from store import OrderStore
from errors import problem, fail

app=Flask(__name__)
store=OrderStore()
STATUS={"pending","confirmed","preparing","ready","delivered","cancelled"}

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

@app.get("/orders")
def list_orders():
    status=request.args.get("status")
    if status and status not in STATUS:
        return fail(problem(400,"Malformed query","Unknown order status."))
    return jsonify({"items":[o.as_json() for o in store.list(status)]}),200

@app.get("/orders/<order_id>")
def get_order(order_id):
    o=store.get(order_id)
    if not o: return fail(problem(404,"Not found","Order does not exist."))
    return jsonify(o.as_json()),200

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
