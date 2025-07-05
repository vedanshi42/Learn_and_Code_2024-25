from abc import ABC, abstractmethod


class IUserRepository(ABC):
    @abstractmethod
    def get_user_by_email(self, email: str):
        pass

    @abstractmethod
    def create_user(self, username, email, hashed_password, role):
        pass
