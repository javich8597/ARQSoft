from contentHandler.models.Content import Content

class TextualContent(Content):
    def __init__(self, text: str):
        super().__init__('text', text)
        self.text = text

    def getNumericalValue(self):
        # Opcionalmente podrías lanzar una excepción o retornar 0
        return 0

    def getTextualValue(self):
        return self.textualvalue
