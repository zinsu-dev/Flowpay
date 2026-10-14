import hashlib
import hmac
import json
import os
from typing import Any

from fastapi import FastAPI
from fastapi import HTTPException, Request
from fastapi.testclient import TestClient
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

class PaystackEvent(BaseModel):
    event: str
    data: dict[str, Any]


@app.post("/webhook/url")
async def verify_webhook(request: Request) -> dict[str, str]:
    secret_key = os.environ.get("PAYSTACK_SECRET_KEY")
    if not secret_key:
        raise HTTPException(
            status_code=500,
            detail="PAYSTACK_SECRET_KEY is not configured",
        )

    body = await request.body()
    signature = request.headers.get("x-paystack-signature", "")
    expected_signature = hmac.new(
        secret_key.encode("utf-8"),
        body,
        hashlib.sha512,
    ).hexdigest()
    if not hmac.compare_digest(signature, expected_signature):
        raise HTTPException(status_code=401, detail="Invalid Paystack signature")

    try:
        event = PaystackEvent.model_validate(json.loads(body))
    except (json.JSONDecodeError, ValueError):
        raise HTTPException(status_code=400, detail="Invalid Paystack event payload")

    return {"status": "success", "event": event.event}


def _signed_payload(secret_key: str, payload: bytes) -> str:
    return hmac.new(secret_key.encode("utf-8"), payload, hashlib.sha512).hexdigest()


def test_verify_webhook_accepts_valid_signed_payload(monkeypatch):
    monkeypatch.setenv("PAYSTACK_SECRET_KEY", "test-secret")
    payload = {"event": "charge.success", "data": {"id": "evt_123"}}
    body = json.dumps(payload).encode("utf-8")
    client = TestClient(app)

    response = client.post(
        "/webhook/url",
        content=body,
        headers={"x-paystack-signature": _signed_payload("test-secret", body)},
    )

    assert response.status_code == 200
    assert response.json() == {"status": "success", "event": "charge.success"}


def test_verify_webhook_rejects_invalid_signature(monkeypatch):
    monkeypatch.setenv("PAYSTACK_SECRET_KEY", "test-secret")
    payload = {"event": "charge.success", "data": {"id": "evt_123"}}
    body = json.dumps(payload).encode("utf-8")
    client = TestClient(app)

    response = client.post(
        "/webhook/url",
        content=body,
        headers={"x-paystack-signature": "not-a-valid-signature"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid Paystack signature"


def test_verify_webhook_rejects_invalid_payload(monkeypatch):
    monkeypatch.setenv("PAYSTACK_SECRET_KEY", "test-secret")
    body = b'{"event": "charge.success"}'
    client = TestClient(app)

    response = client.post(
        "/webhook/url",
        content=body,
        headers={"x-paystack-signature": _signed_payload("test-secret", body)},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid Paystack event payload"


def test_verify_webhook_requires_configured_secret(monkeypatch):
    monkeypatch.delenv("PAYSTACK_SECRET_KEY", raising=False)
    client = TestClient(app)

    response = client.post(
        "/webhook/url",
        content=b'{"event": "charge.success", "data": {"id": "evt_123"}}',
        headers={"x-paystack-signature": "ignored"},
    )

    assert response.status_code == 500
    assert response.json()["detail"] == "PAYSTACK_SECRET_KEY is not configured"
