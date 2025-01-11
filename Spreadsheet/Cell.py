from ContentHandler.Models.Content import Content

class Cell:
    def __init__(self, position: str, content: Content):
        self.position = position
        self.content = content

    def get_content(self):
        return self.content.getValue()
