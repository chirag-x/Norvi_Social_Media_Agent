from abc import ABC, abstractmethod
from typing import List
from pydantic import BaseModel

class VideoResult(BaseModel):
    id: str
    title: str
    url: str
    channel: str
    views: int
    publish_date: str
    duration: str
    thumbnail: str
    niche: str

class DiscoveryProvider(ABC):
    """
    Abstract base class for content discovery providers (e.g., YouTube).
    """
    @abstractmethod
    async def search(self, query: str, niche: str, max_results: int = 10) -> List[VideoResult]:
        pass
