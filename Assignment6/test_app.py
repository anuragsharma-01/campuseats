import sys, os, pytest
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
from app import app, store, rate_limits

@pytest.fixture(autouse=True)
def clean():
    store.orders.clear()
    store.idempotency.clear()
    rate_limits.clear()
    yield
    store.orders.clear()
    store.idempotency.clear()
    rate_limits.clear()

@pytest.fixture
def client():
    app.config["TESTING"]=True
    return app.test_client()

def data():
    return {"customer_id":"student-17","restaurant_id":"rest-2",
            "items":[{"menu_item_id":"m-101","quantity":2}],
            "delivery_address":"Hostel A"}

def test_create_201_location(monkeypatch,client):
    monkeypatch.setattr("app.authorize_payment",lambda *a: None)
    r=client.post("/orders",json=data(),headers={
    "Idempotency-Key":"order-1",
    "Authorization":"Bearer test-token"
})
    assert r.status_code==201
    assert r.headers["Location"].startswith("/orders/")
    assert "internal_payment_reference" not in r.json

def test_idempotent_repeat(monkeypatch,client):
    monkeypatch.setattr("app.authorize_payment",lambda *a: None)
    h={
    "Idempotency-Key":"same-key",
    "Authorization":"Bearer test-token"
}
    a=client.post("/orders",json=data(),headers=h)
    b=client.post("/orders",json=data(),headers=h)
    assert a.status_code==b.status_code==201
    assert a.json["id"]==b.json["id"]

def test_malformed_400(client):
    r=client.post("/orders",json={"customer_id":"student-17"},
                  headers={
    "Idempotency-Key":"x",
    "Authorization":"Bearer test-token"
})
    assert r.status_code==400
    assert set(r.json)=={"type","title","status","detail"}

def test_unknown_404(client):
    assert client.get("/orders/no-such-id").status_code==404

def test_state_conflict(monkeypatch,client):
    monkeypatch.setattr("app.authorize_payment",lambda *a: None)
    r=client.post("/orders",json=data(),headers={
    "Idempotency-Key":"x",
    "Authorization":"Bearer test-token"
})
    oid=r.json["id"]
    assert client.post(
    f"/orders/{oid}/cancellation",
    headers={"Authorization": "Bearer test-token"}
).status_code == 202
    assert client.post(
    f"/orders/{oid}/cancellation",
    headers={"Authorization": "Bearer test-token"}
).status_code == 409
def test_missing_authorization_returns_401(client):
    r = client.post(
        "/orders",
        json=data(),
        headers={"Idempotency-Key": "auth-test"}
    )
    assert r.status_code == 401

def test_etag_and_conditional_get(monkeypatch, client):
    monkeypatch.setattr("app.authorize_payment", lambda *a: None)

    r = client.post(
        "/orders",
        json=data(),
        headers={
            "Idempotency-Key": "etag-test",
            "Authorization": "Bearer test-token"
        }
    )

    assert r.status_code == 201

    oid = r.json["id"]

    first = client.get(f"/orders/{oid}")

    assert first.status_code == 200
    assert first.headers.get("ETag")
    assert first.headers.get("Cache-Control")

    etag = first.headers["ETag"]

    second = client.get(
        f"/orders/{oid}",
        headers={"If-None-Match": etag}
    )

    assert second.status_code == 304
    assert second.headers["ETag"] == etag
    assert second.data == b""
def test_if_match_stale_etag_returns_412(monkeypatch, client):
    monkeypatch.setattr(
        "app.authorize_payment",
        lambda *a: None
    )

    r = client.post(
        "/orders",
        json=data(),
        headers={
            "Idempotency-Key": "if-match-test",
            "Authorization": "Bearer test-token"
        }
    )

    assert r.status_code == 201
    oid = r.json["id"]

    current = client.get(f"/orders/{oid}")
    assert current.status_code == 200

    etag = current.headers["ETag"]

    update = client.patch(
        f"/orders/{oid}",
        json={"status": "preparing"},
        headers={
            "Authorization": "Bearer test-token",
            "If-Match": etag
        }
    )

    assert update.status_code == 200

    new_etag = update.headers["ETag"]
    assert new_etag != etag

    stale = client.patch(
        f"/orders/{oid}",
        json={"status": "ready"},
        headers={
            "Authorization": "Bearer test-token",
            "If-Match": etag
        }
    )

    assert stale.status_code == 412