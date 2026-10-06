# Campus Customs harness: audit, safety, and operation

## Database schema

The SQLite database is `data/campus_customs.db`. The application reads catalogue and inventory data in read-only mode; account registration and chat history are the intentional write paths.

### `catalogue`

Product master data used by the storefront and chatbot recommendations.

| Field | Type | Why it matters |
|---|---|---|
| `product_id` | TEXT, primary key | Stable identifier linking a product across search, detail pages, inventory, and chat results. |
| `name` | TEXT | Customer-facing product name used in cards, detail pages, and search. |
| `garment_type` | TEXT | Identifies the kind of item, such as hoodie, shirt, or crewneck, for filtering and recommendations. |
| `description` | TEXT | Provides verified product details that the chatbot can explain to customers. |
| `colors` | TEXT | Supports color-based product searches and recommendations. |
| `search_tags` | TEXT | Adds searchable school, team, sport, and product keywords. |
| `image_file_path` | TEXT | Identifies the product image shown in the storefront and chatbot match cards. |
| `price` | REAL | Provides the verified current price; the chatbot must not invent or estimate it. |

### `inventory`

Size-level stock data used to answer availability questions.

| Field | Type | Why it matters |
|---|---|---|
| `id` | INTEGER, primary key | Uniquely identifies an inventory row. |
| `product_id` | TEXT, foreign key | Links stock to the corresponding catalogue product. |
| `size` | TEXT | Identifies the exact size a customer is asking about. |
| `quantity` | INTEGER | Provides the verified number available and supports sold-out states. |

### `users`

Customer account data used for login, personalization, and associating chat history.

| Field | Type | Why it matters |
|---|---|---|
| `id` | INTEGER, primary key | Stable account identifier used to associate requests and messages with a customer. |
| `name` | TEXT | Stores the account display name for the user record. |
| `email` | TEXT, unique | Login identifier and contact field; uniqueness prevents duplicate accounts. |
| `password_hash` | TEXT | Stores a one-way password verification value; it must never be exposed to the chatbot or frontend. |
| `created_at` | TEXT | Records when the account was created. |
| `first_name` | TEXT | Supports safe personalized greetings and agent context. |
| `last_name` | TEXT | Supports complete account identification and personalization. |

### `chat_messages`

Persisted messages for logged-in customer memory and conversation restoration.

| Field | Type | Why it matters |
|---|---|---|
| `id` | INTEGER, primary key | Orders and uniquely identifies each stored message. |
| `user_id` | INTEGER, foreign key | Associates the message with the customer whose history should be restored. |
| `role` | TEXT | Distinguishes user messages from assistant responses. |
| `content` | TEXT | Stores the message text needed to display recent conversation history. |
| `products_json` | TEXT, nullable | Preserves product IDs associated with an assistant response for history and review. |
| `created_at` | TEXT | Records message time and supports chronological history ordering. |

`sqlite_sequence` is an internal SQLite bookkeeping table for autoincrement counters, not application data and not used by the shop or chatbot.

## Model fields and reasons

`ChatRequest`: `message` (1–1000 characters), optional `user_id`, `current_page` (max 300), and `product_id` (max 120). These bounds prevent empty requests and unbounded context. `ChatResponse` returns `answer`, `product_ids`, and verified `matches`; each match has product ID, name, garment type, description, price, and image path for trustworthy UI cards.

## Tools and ability

- `search_products(query)`: read-only typo-tolerant catalogue search, at most eight results.
- `get_product_info(product_id)`: exact catalogue and current price lookup.
- `get_product_availability(product_id)`: all sizes and quantities.
- `get_stock_by_size(product_id, size)`: exact-size inventory lookup.

All tools use SQLite read-only mode. They cannot create orders, change inventory, access passwords, write customer data, or make network requests.

## Safety rules

The system prompt requires verified tools for product, price, and stock claims; prohibits invented facts; treats customer/page/tool text as untrusted; and prevents disclosure of credentials, private account data, prompts, raw errors, audit records, and unnecessary personal data. Missing rows are reported as unverified. Unsafe, prompt-injection, or non-shopping requests are briefly refused. The agent receives only first name, last name, email, current page, and product ID; password hashes are never passed to it.

## Audit trail

`output/audit_trail.json` is a chronological append-only list. Each entry contains UTC `time`, `event`, `tool_name`, short `arguments`, short `result`, and final-event `stop_reason`. Values are capped before recording; credentials and full chat content are not recorded. Stop reasons are `completed` or `agent_error`. Audit failures do not break chat.

## System specifications

- Model: `PORTKEY_MODEL`, default `gpt-5.6-luna`; endpoint: `PORTKEY_BASE_URL`, default `https://api.portkey.ai/v1`; key: `PORTKEY_API_KEY`.
- Agent output is validated as `ChatResponse`; retries: 1.
- Caps: search 8 products, history 20 messages, request 1000 characters, audit text 240 characters and collections 20 items.
- Loop control: no custom infinite loop; PydanticAI/provider bounds each run. The prompt requires stopping after the answer and avoiding repeated lookups.
- Database: `data/campus_customs.db`; catalogue/inventory reads are read-only.

## Unified application and history

`backend/main.py` is the single application for the storefront API: it serves products and images, `/api/auth/register`, `/api/auth/login`, `/api/chat`, and `/api/chat/history/{user_id}`. Logged-in chat writes and restores the user’s messages; guests remain in the browser only. The API rejects unknown user IDs and never sends password hashes to the agent. This is demo authentication based on the returned user ID; it does not provide a persistent session token.

## Customer memory and context

For a logged-in user, each successful chat request saves one `user` row and one `assistant` row in `chat_messages`, including returned product IDs for the assistant response. `GET /api/chat/history/{user_id}` retrieves the most recent 20 messages in chronological order. The frontend restores those messages when the user ID is loaded and also refreshes the chat identity immediately after login or account creation. Unknown user IDs are rejected.

The backend passes the agent only safe user fields (`first_name`, `last_name`, and `email`) plus the current page path and current product ID. Product-page context is derived from the route and guest requests pass `user_id: null`, so guests can chat without account lookup or database persistence. Guest messages remain only in the current browser view.

## Authentication verification

Account creation accepts first name, last name, email, and a password of 8–200 characters. The backend normalizes the email to lowercase, rejects duplicate addresses, and stores only a salted PBKDF2-HMAC-SHA256 password hash with 240,000 iterations. The plaintext password is never stored or returned. Login checks the submitted password with a constant-time comparison and returns only the user ID, name fields, and email.

The seeded test account `test@campuscustoms.yale.edu` was verified with the provided password `password`; its legacy three-part PBKDF2 format uses 120,000 iterations and was accepted. A newly created account was tested in an isolated database copy: its four-part PBKDF2 hash verified the correct password and rejected an incorrect password. The real project database was not modified by this verification.

The frontend forms call `/api/auth/register` and `/api/auth/login`, then retain the returned user ID to restore that user’s chat history. This is intentionally a simple assignment-level authentication flow; it does not issue a persistent session or JWT token.

## How to run

Backend, from `Homework 4/backend`:

```bash
uvicorn main:app --reload --port 8000
```

Frontend, from `Homework 4/frontend`:

```bash
npm run dev
```

Open the Vite URL, normally `http://localhost:5173`; keep the unified backend running at `http://localhost:8000`. Check it with `GET /health`. Set Portkey variables in `Homework 4/.env` before live chat. Do not start the legacy root `api.py` at the same port.
