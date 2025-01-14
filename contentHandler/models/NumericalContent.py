from contentHandler.models.Content import Content

class NumericalContent(Content):
    def __init__(self, number: float):
        super().__init__('number', str(number))

    def getNumericalValue(self):
        return float(self.textualvalue)

    def getTextualValue(self):
        return self.getValue()
