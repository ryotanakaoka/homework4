from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)
    user_id: int | None = None
    current_page: str | None = Field(default=None, max_length=300)
    product_id: str | None = Field(default=None, max_length=120)


class RegisterRequest(BaseModel):
    first_name: str = Field(min_length=1, max_length=80)
    last_name: str = Field(min_length=1, max_length=80)
    email: str = Field(min_length=3, max_length=320)
    password: str = Field(min_length=8, max_length=200)


class LoginRequest(BaseModel):
    email: str = Field(min_length=3, max_length=320)
    password: str = Field(min_length=1, max_length=200)


class ChatResponse(BaseModel):
    answer: str
    product_ids: list[str] = Field(default_factory=list)
    matches: list["ProductHit"] = Field(default_factory=list)


class ProductHit(BaseModel):
    product_id: str
    name: str
    garment_type: str
    description: str
    price: float
    image_file_path: str


class InventoryItem(BaseModel):
    product_id: str
    size: str
    quantity: int


class ProductInfo(BaseModel):
    """Verified catalogue facts returned to the chatbot."""

    product_id: str
    name: str
    garment_type: str
    description: str
    colors: str
    search_tags: str
    price: float
    image_file_path: str


class StockBySize(BaseModel):
    """Verified stock quantity for one product size."""

    product_id: str
    size: str
    quantity: int
