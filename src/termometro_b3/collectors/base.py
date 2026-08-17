from abc import ABC, abstractmethod

from termometro_b3.models import NewsArticle


class BaseCollector(ABC):
    @abstractmethod
    def collect(self) -> list[NewsArticle]:
        """Collect news articles from a source."""
        raise NotImplementedError
