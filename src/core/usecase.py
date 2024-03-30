from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class UseCase(ABC):
    @abstractmethod
    def execute(self, request: Any) -> Any:
        raise NotImplementedError
