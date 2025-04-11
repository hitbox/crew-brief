from abc import ABC
from abc import abstractmethod

class Process(ABC):
    """
    Abstract class requiring a run method.
    """

    @abstractmethod
    def run(self):
        pass
