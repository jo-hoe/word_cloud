from abc import ABC, abstractmethod
from typing import List


class InputSourceStrategy(ABC):
    @abstractmethod
    def extract_texts(self, input_source: str) -> List[str]:
        """
        Extract plain text snippets from the given input source.
        Implementations should return a list of message strings (without metadata).
        """
        pass
