from abc import ABC, abstractmethod
from typing import Dict


class IArticleCategorizer(ABC):
    @abstractmethod
    def categorize(self, article: Dict):
        pass
