from dataclasses import dataclass


@dataclass
class User:
    user_id: int
    username: str
    email: str
    role: str
