from contentHandler.models.Content import Content

class NumericalContent(Content):
    def __init__(self, number: float):
        super().__init__('number', str(number))
        self.number = number

    def getNumericalValue(self):
        return self.number

    def get_content(self):
        return f"Numero: {self.textualvalue}"