from abc import ABC, abstractmethod


class IExternalAPIRepository(ABC):
    @abstractmethod
    def update_status(self, name: str, status: str):
        pass

    @abstractmethod
    def get_last_accessed(self, name: str):
        pass

    @abstractmethod
    def get_all_statuses(self, name: str):
        pass
