from dataclasses import dataclass
from datetime import datetime
from pydantic import BaseModel


@dataclass
class Article:
    title: str
    content: str
    source_url: str
    date_published: datetime
    category: str


class ArticleActionRequest(BaseModel):
    user_id: int
    article_id: int
