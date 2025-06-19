from dataclasses import dataclass
from datetime import datetime


@dataclass
class Article:
    title: str
    content: str
    source_url: str
    date_published: datetime
    category: str
