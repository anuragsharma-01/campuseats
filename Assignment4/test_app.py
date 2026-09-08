import sys, os, pytest
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
from app import app, store

@pytest.fixture(autouse=True)
def clean():
    store.orders.clear(); store.idempotency.clear()
    yield
    store.orders.clear(); store.idempotency.clear()

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
    r=client.post("/orders",json=data(),headers={"Idempotency-Key":"order-1"})
    assert r.status_code==201
    assert r.headers["Location"].startswith("/orders/")
    assert "internal_payment_reference" not in r.json

def test_idempotent_repeat(monkeypatch,client):
    monkeypatch.setattr("app.authorize_payment",lambda *a: None)
    h={"Idempotency-Key":"same-key"}
    a=client.post("/orders",json=data(),headers=h)
    b=client.post("/orders",json=data(),headers=h)
    assert a.status_code==b.status_code==201
    assert a.json["id"]==b.json["id"]

def test_malformed_400(client):
    r=client.post("/orders",json={"customer_id":"student-17"},
                  headers={"Idempotency-Key":"x"})
    assert r.status_code==400
    assert set(r.json)=={"type","title","status","detail"}

def test_unknown_404(client):
    assert client.get("/orders/no-such-id").status_code==404

def test_state_conflict(monkeypatch,client):
    monkeypatch.setattr("app.authorize_payment",lambda *a: None)
    r=client.post("/orders",json=data(),headers={"Idempotency-Key":"x"})
    oid=r.json["id"]
    assert client.post(f"/orders/{oid}/cancellation").status_code==202
    assert client.post(f"/orders/{oid}/cancellation").status_code==409
