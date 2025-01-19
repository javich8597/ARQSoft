from abc import ABC, abstractmethod

class Content(ABC):
    """Abstract Class representing the content of a cell in a spreadsheet."""
    
    def __init__(self, type: str, stringvalue: str) -> None:
        self.type = type
        self.textualvalue = stringvalue

    @abstractmethod
    def get_number_value(self) -> float:
        pass

    @abstractmethod
    def get_content(self):
        pass
    
    def get_value(self) -> str:
        return self.textualvalue
