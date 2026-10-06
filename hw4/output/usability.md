# Usability Improvements

Problem 9 contains exactly four improvements: two in the frontend and two in the agent/backend.

## Frontend improvements

### 1. Catalogue search field

The Products page includes a search field that filters the loaded catalogue by product name, garment type, school, team, and other search tags. Results update immediately as the customer types, making a large collection faster to browse.

### 2. Clear loading, error, and empty-result feedback

The Products and product-detail pages show loading messages while requests are in progress. Failed product requests show an actionable server message, invalid product pages explain that the item was not found, and searches with no matches suggest trying another search. These states prevent blank pages and give customers a clear next step.

## Agent/backend improvements

### 3. Partial and typo-tolerant chatbot search

`search_products` compares customer terms against product names, garment types, descriptions, colors, and search tags. It supports partial terms, similar spellings, and returns no more than eight ranked matches. This makes natural-language product discovery more forgiving while keeping recommendations tied to catalogue records.

### 4. Helpful missing-product and missing-size responses

The agent prompt requires the assistant to explain when a product or requested size has no verified database record, suggest a clearer search when appropriate, and never substitute a different size or invent a price or quantity. This helps customers recover from an unsuccessful lookup while preserving factual accuracy.

## Verification

The frontend implementation is in `frontend/src/main.tsx`; the backend search behavior is in `backend/tools.py`; and the response rules are in `backend/prompts/prompt.md`. The frontend TypeScript check passes with `npx tsc --noEmit`. The Problem 11 app check also captures the category-search cards and missing-product feedback scenarios.
