from abc import ABC, abstractmethod
from pathlib import Path


class Engine(ABC):
    @abstractmethod
    def generate_html(self, fp: Path, template: str = None) -> str:
        raise NotImplementedError
