from pathlib import Path
import sqlite3
from typing import Any
from difflib import SequenceMatcher

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "campus_customs.db"


def _query(sql: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    """Run a read-only query against the shop database."""
    with sqlite3.connect(f"file:{DB.resolve()}?mode=ro", uri=True) as con:
        con.row_factory = sqlite3.Row
        return [dict(row) for row in con.execute(sql, params)]


def search_products(query: str) -> list[dict[str, Any]]:
    """Search catalogue products with partial and typo-tolerant matching."""
    terms = [term.strip().lower() for term in query.split() if term.strip()]
    if not terms:
        return []
    rows = _query("SELECT product_id, name, garment_type, description, colors, search_tags, price, image_file_path FROM catalogue")
    scored = []
    for row in rows:
        text = " ".join(str(row[field] or "") for field in ("name", "garment_type", "description", "colors", "search_tags")).lower()
        score = 0.0
        for term in terms[:6]:
            if term in text:
                score += 2.0
            else:
                score += max((SequenceMatcher(None, term, word).ratio() for word in text.split()), default=0.0)
        if score >= 0.75:
            scored.append((score, row))
    scored.sort(key=lambda item: (-item[0], item[1]["name"]))
    return [{key: row[key] for key in ("product_id", "name", "garment_type", "description", "price", "image_file_path")} for _, row in scored[:8]]


def get_product_availability(product_id: str) -> list[dict[str, Any]]:
    """Return size and quantity information for one catalogue product."""
    return _query("SELECT product_id, size, quantity FROM inventory WHERE product_id = ? ORDER BY size", (product_id,))


def get_product_info(product_id: str) -> list[dict[str, Any]]:
    """Return verified catalogue details, including the current database price."""
    return _query("SELECT product_id, name, garment_type, description, colors, search_tags, price, image_file_path FROM catalogue WHERE product_id = ?", (product_id,))


def get_stock_by_size(product_id: str, size: str) -> list[dict[str, Any]]:
    """Return verified stock for one exact product and size; an empty list means no record was found."""
    return _query("SELECT product_id, size, quantity FROM inventory WHERE product_id = ? AND lower(size) = lower(?)", (product_id, size.strip()))


def get_user_context(user_id: int) -> dict[str, Any] | None:
    """Return only safe display fields for a logged-in user."""
    rows = _query("SELECT id, first_name, last_name, email FROM users WHERE id = ?", (user_id,))
    return rows[0] if rows else None


def get_chat_history(user_id: int, limit: int = 20) -> list[dict[str, Any]]:
    """Load recent persisted messages for one user, oldest first."""
    rows = _query("SELECT role, content, created_at FROM chat_messages WHERE user_id = ? ORDER BY id DESC LIMIT ?", (user_id, limit))
    return list(reversed(rows))


def save_chat_message(user_id: int, role: str, content: str, products_json: str | None = None) -> None:
    """Persist one chat message for a logged-in user."""
    with sqlite3.connect(DB) as con:
        con.execute("INSERT INTO chat_messages (user_id, role, content, products_json, created_at) VALUES (?, ?, ?, ?, datetime('now'))", (user_id, role, content, products_json))
        con.commit()
