from pydantic import BaseModel


class EmailPayload(BaseModel):
    email: str


class ToggleCategoryPayload(BaseModel):
    user_id: int
    category: str


class ToggleKeywordPayload(BaseModel):
    user_id: int
    keyword: str
