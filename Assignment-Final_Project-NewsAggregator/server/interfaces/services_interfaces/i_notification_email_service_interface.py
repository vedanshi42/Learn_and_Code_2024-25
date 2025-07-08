from abc import ABC, abstractmethod


class INotificationEmailService(ABC):
    @abstractmethod
    def send_notifications_to_all_users(self):
        pass
