from abc import ABC, abstractmethod


class IAuthService(ABC):
    @abstractmethod
    def login(self, email, password):
        pass

    @abstractmethod
    def register(self, user_data):
        pass

    @abstractmethod
    def logout(self, user_id):
        pass
