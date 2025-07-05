from abc import ABC, abstractmethod
from typing import List, Dict


class INotificationRepository(ABC):

    @abstractmethod
    def replace_notifications_for_user(self, user_id: int, articles: List[Dict]):
        pass

    @abstractmethod
    def get_notifications_for_user(self, user_id: int):
        pass
