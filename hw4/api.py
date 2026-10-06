from pathlib import Path
import sqlite3
import base64
import hashlib
import hmac
import os
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

ROOT = Path(__file__).parent
DB = ROOT / "data" / "campus_customs.db"
app = FastAPI(title="Campus Customs API")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_methods=["*"], allow_headers=["*"])
app.mount("/images", StaticFiles(directory=ROOT / "data" / "products"), name="images")

def query(sql: str, params: tuple = ()):
    with sqlite3.connect(f"file:{DB.resolve()}?mode=ro", uri=True) as con:
        con.row_factory = sqlite3.Row
        return [dict(row) for row in con.execute(sql, params)]

class RegisterRequest(BaseModel):
    first_name: str = Field(min_length=1, max_length=80)
    last_name: str = Field(min_length=1, max_length=80)
    email: EmailStr
    password: str = Field(min_length=8, max_length=200)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=200)

def password_hash(password: str, salt: bytes | None = None) -> str:
    salt = salt or os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 240_000)
    return f"pbkdf2_sha256$240000${base64.urlsafe_b64encode(salt).decode()}${base64.urlsafe_b64encode(digest).decode()}"

def password_matches(password: str, stored: str) -> bool:
    try:
        parts = stored.split("$")
        if len(parts) == 3:
            # Compatibility with the seeded Homework 4 users.
            scheme, salt_text, digest_text = parts
            rounds = 120_000
        else:
            scheme, rounds, salt_text, digest_text = parts
        if scheme != "pbkdf2_sha256":
            return False
        if len(parts) == 3:
            salt = salt_text.encode()
            expected = bytes.fromhex(digest_text)
        else:
            salt = base64.urlsafe_b64decode(salt_text.encode())
            expected = base64.urlsafe_b64decode(digest_text.encode())
        actual = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, int(rounds))
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False

def write(sql: str, params: tuple = ()) -> None:
    with sqlite3.connect(DB) as con:
        con.execute(sql, params)
        con.commit()

@app.get("/api/products")
def products():
    return query("SELECT product_id, name, garment_type, description, colors, search_tags, image_file_path, price FROM catalogue ORDER BY name")

@app.get("/api/products/{product_id}")
def product(product_id: str):
    rows = query("SELECT product_id, name, garment_type, description, colors, search_tags, image_file_path, price FROM catalogue WHERE product_id = ?", (product_id,))
    if not rows:
        raise HTTPException(404, "Product not found")
    inventory = query("SELECT size, quantity FROM inventory WHERE product_id = ? ORDER BY size", (product_id,))
    return {"product": rows[0], "inventory": inventory}

@app.post("/api/auth/register", status_code=201)
def register(request: RegisterRequest):
    email = str(request.email).lower()
    if query("SELECT id FROM users WHERE lower(email) = ?", (email,)):
        raise HTTPException(409, "An account with this email already exists")
    first_name, last_name = request.first_name.strip(), request.last_name.strip()
    write("INSERT INTO users (name, email, password_hash, created_at, first_name, last_name) VALUES (?, ?, ?, ?, ?, ?)", (f"{first_name} {last_name}", email, password_hash(request.password), datetime.now(timezone.utc).isoformat(), first_name, last_name))
    user = query("SELECT id, first_name, last_name, email FROM users WHERE email = ?", (email,))[0]
    return {"message": "Account created", "user": user}

@app.post("/api/auth/login")
def login(request: LoginRequest):
    email = str(request.email).lower()
    rows = query("SELECT id, first_name, last_name, email, password_hash FROM users WHERE lower(email) = ?", (email,))
    if not rows or not password_matches(request.password, rows[0]["password_hash"]):
        raise HTTPException(401, "Invalid email or password")
    user = {key: rows[0][key] for key in ("id", "first_name", "last_name", "email")}
    return {"message": "Login successful", "user": user}
