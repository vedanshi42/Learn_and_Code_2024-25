from pydantic import BaseModel


class UpdateKeyRequest(BaseModel):
    api_name: str
    api_key: str


class CategoryRequest(BaseModel):
    name: str


class KeywordRequest(BaseModel):
    word: str


class DeleteArticleRequest(BaseModel):
    user_id: int
