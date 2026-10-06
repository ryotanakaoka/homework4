from pathlib import Path
import sqlite3
import base64
import hashlib
import hmac
import os
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles

from agent import shop_agent
from models import ChatRequest, ChatResponse, LoginRequest, RegisterRequest
from tools import get_chat_history, get_user_context, save_chat_message, _query
from audit import record

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "campus_customs.db"

app = FastAPI(title="Campus Customs Chatbot")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175", "http://127.0.0.1:5173", "http://127.0.0.1:5175"], allow_methods=["*"], allow_headers=["*"])
app.mount("/images", StaticFiles(directory=ROOT / "data" / "products"), name="images")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/products")
def products() -> list[dict]:
    return _query("SELECT product_id, name, garment_type, description, colors, search_tags, image_file_path, price FROM catalogue ORDER BY name")


@app.get("/api/products/{product_id}")
def product(product_id: str) -> dict:
    rows = _query("SELECT product_id, name, garment_type, description, colors, search_tags, image_file_path, price FROM catalogue WHERE product_id = ?", (product_id,))
    if not rows:
        raise HTTPException(404, "Product not found")
    return {"product": rows[0], "inventory": _query("SELECT size, quantity FROM inventory WHERE product_id = ? ORDER BY size", (product_id,))}


def _password_hash(password: str, salt: bytes | None = None) -> str:
    salt = salt or os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 240_000)
    return f"pbkdf2_sha256$240000${base64.urlsafe_b64encode(salt).decode()}${base64.urlsafe_b64encode(digest).decode()}"


def _password_matches(password: str, stored: str) -> bool:
    try:
        parts = stored.split("$")
        if len(parts) == 3:
            scheme, salt_text, digest_text = parts
            rounds = 120_000
            salt = salt_text.encode()
            expected = bytes.fromhex(digest_text)
        else:
            scheme, rounds, salt_text, digest_text = parts
            salt = base64.urlsafe_b64decode(salt_text.encode())
            expected = base64.urlsafe_b64decode(digest_text.encode())
        if scheme != "pbkdf2_sha256":
            return False
        actual = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, int(rounds))
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


@app.post("/api/auth/register", status_code=201)
def register(request: RegisterRequest) -> dict:
    first_name = request.first_name.strip()
    last_name = request.last_name.strip()
    email = request.email.strip().lower()
    password = request.password
    if "@" not in email:
        raise HTTPException(422, "A valid email is required")
    if _query("SELECT id FROM users WHERE lower(email) = ?", (email,)):
        raise HTTPException(409, "An account with this email already exists")
    with sqlite3.connect(DB) as con:
        con.execute("INSERT INTO users (name, email, password_hash, created_at, first_name, last_name) VALUES (?, ?, ?, ?, ?, ?)", (f"{first_name} {last_name}", email, _password_hash(password), datetime.now(timezone.utc).isoformat(), first_name, last_name))
        con.commit()
    return {"message": "Account created", "user": _query("SELECT id, first_name, last_name, email FROM users WHERE email = ?", (email,))[0]}


@app.post("/api/auth/login")
def login(request: LoginRequest) -> dict:
    email = request.email.strip().lower()
    password = request.password
    rows = _query("SELECT id, first_name, last_name, email, password_hash FROM users WHERE lower(email) = ?", (email,))
    if not rows or not _password_matches(password, rows[0]["password_hash"]):
        raise HTTPException(401, "Invalid email or password")
    user = {key: rows[0][key] for key in ("id", "first_name", "last_name", "email")}
    return {"message": "Login successful", "user": user}


@app.get("/api/chat/history/{user_id}")
def history(user_id: int) -> dict[str, list[dict]]:
    if not get_user_context(user_id):
        raise HTTPException(404, "User not found")
    return {"messages": get_chat_history(user_id)}


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    user = get_user_context(request.user_id) if request.user_id is not None else None
    if request.user_id is not None and user is None:
        raise HTTPException(404, "User not found")
    context = {
        "customer": {key: user[key] for key in ("first_name", "last_name", "email")} if user else "guest",
        "current_page": request.current_page,
        "current_product_id": request.product_id,
    }
    prompt = f"Customer and page context (use only for helpful personalization): {context}\nCustomer message: {request.message}"
    record(event="start", tool_name="agent", arguments={"user_id": request.user_id, "current_page": request.current_page})
    try:
        result = shop_agent.run_sync(prompt).output
    except Exception as exc:
        record(event="stop", tool_name="agent", arguments={"user_id": request.user_id}, result=str(exc), stop_reason="agent_error")
        raise HTTPException(502, "The shopping assistant is temporarily unavailable") from exc
    if user:
        import json
        save_chat_message(user["id"], "user", request.message)
        save_chat_message(user["id"], "assistant", result.answer, json.dumps(result.product_ids))
    record(event="stop", tool_name="agent", arguments={"user_id": request.user_id}, result={"product_ids": result.product_ids}, stop_reason="completed")
    return result
