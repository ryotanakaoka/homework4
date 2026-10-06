import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from models import ChatResponse
from tools import get_product_availability, get_product_info, get_stock_by_size, search_products
from audit import record

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

provider = OpenAIProvider(
    base_url=os.getenv("PORTKEY_BASE_URL", "https://api.portkey.ai/v1"),
    api_key=os.getenv("PORTKEY_API_KEY"),
)
model = OpenAIChatModel(os.getenv("PORTKEY_MODEL", "gpt-5.6-luna"), provider=provider)

def _logged(tool, **kwargs):
    try:
        result = tool(**kwargs)
        record(event="tool", tool_name=tool.__name__, arguments=kwargs, result=result)
        return result
    except Exception as exc:
        record(event="tool_error", tool_name=tool.__name__, arguments=kwargs, result=str(exc))
        raise

def logged_search_products(query: str): return _logged(search_products, query=query)
def logged_get_product_info(product_id: str): return _logged(get_product_info, product_id=product_id)
def logged_get_product_availability(product_id: str): return _logged(get_product_availability, product_id=product_id)
def logged_get_stock_by_size(product_id: str, size: str): return _logged(get_stock_by_size, product_id=product_id, size=size)
shop_agent = Agent(
    model=model,
    output_type=ChatResponse,
    system_prompt=(Path(__file__).parent / "prompts" / "prompt.md").read_text(encoding="utf-8"),
    tools=[logged_search_products, logged_get_product_info, logged_get_product_availability, logged_get_stock_by_size],
    retries=1,
)
