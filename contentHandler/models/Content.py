from abc import ABC, abstractmethod

class Content(ABC):
    """Clase base para diferentes tipos de contenido en una celda."""
    
    def __init__(self, type: str, stringvalue: str) -> None:
        self.type = type
        self.textualvalue = stringvalue

    @abstractmethod
    def getNumericalValue(self) -> float:
        pass

    @abstractmethod
    def get_content(self):
        pass
    
    def getValue(self) -> str:
        return self.textualvalue
