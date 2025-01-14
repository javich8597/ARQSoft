from contentHandler.models.Content import Content

class NumericalContent(Content):
    def __init__(self, number: float):
        super().__init__('number', str(number))
        self.number = number

    def getNumericalValue(self):
        return self.number

    def getTextualValue(self):
        return self.textualvalue
