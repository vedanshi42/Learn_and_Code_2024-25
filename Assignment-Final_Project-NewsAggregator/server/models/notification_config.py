from dataclasses import dataclass
from datetime import datetime


@dataclass
class Notification:
    article_id: int
    title: str
    date_published: datetime
