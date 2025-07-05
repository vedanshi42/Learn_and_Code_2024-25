from abc import ABC, abstractmethod


class INotificationUpdater(ABC):
    @abstractmethod
    def update_notifications_for_all_users(self):
        pass
