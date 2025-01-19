from contentHandler.models.Content import Content

class TextualContent(Content):
    def __init__(self, text: str):
        super().__init__('text', text)

    def get_number_value(self):
        # Opcionalmente podrías lanzar una excepción o retornar 0
        return 0

    def get_content(self):
        return f"Text: {self.textualvalue}"
