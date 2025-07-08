from abc import ABC, abstractmethod


class IAuthService(ABC):
    @abstractmethod
    def login(self, email, password):
        pass

    @abstractmethod
    def signup(self, username, email, password):
        pass
