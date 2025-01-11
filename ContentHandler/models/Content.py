from abc import ABC, abstractmethod

class Content(ABC):
    """Clase base para diferentes tipos de contenido en una celda."""
    
    def __init__(self, type: str, stringvalue: str) -> None:
        self.type = type
        self.textualvalue = stringvalue

    @abstractmethod
    def getNumericalValue(self):
        pass

    @abstractmethod
    def getTextualValue(self):
        pass
    
    def getValue(self) -> str:
        return self.textualvalue
    
    def typeContent(self) -> str:
        return self.type
