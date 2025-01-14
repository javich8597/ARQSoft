from contentHandler.models.NumericalContent import NumericalContent
from contentHandler.models.FormulaContent import FormulaContent
from contentHandler.models.TextualContent import TextualContent

class Cell:
    """
    Represents a single cell within a spreadsheet.
    """

    def __init__(self, row: int, col: str, content=None):
        """
        Initializes a cell with its coordinates and optional content.
        """
        self.row = row
        self.col = col
        self.content = self._identify_content(content)  # Raw content of the cell (e.g., number, text, formula)
        self.value = None  # Evaluated value of the cell (e.g., formula result)

    def _identify_content(self, content):
        """
        Identifies the type of content and returns the appropriate content object.
        """
        if content is None:
            return None
        if isinstance(content, (int, float)):
            return NumericalContent(content)
        elif isinstance(content, str) and content.startswith("="):
            return FormulaContent(content[1:], None)
        else:
            return TextualContent(content)

    def getCoordinate(self):
        """
        Returns the coordinates of the cell as a tuple (row, col).
        """
        return self.row, self.col

    def setCoordinate(self, row: int, col: str):
        """
        Sets the coordinates of the cell composed by row and column.
        """

        if not isinstance(row, int) or row <= 0:
            raise ValueError("Row must be a positive integer.")
        if not isinstance(col, str) or not col.isalpha():
            raise ValueError("Column must be a string containing only letters.")
        
        self.row = row
        self.col = col

    def getContent(self):
        """
        Gets the raw content of the cell.
        """
        return self.content

    def setContent(self, content):
        """
        Sets the raw content of the cell.
        """
        self.content = self._identify_content(content)

    def getValue(self):
        """
        Returns the evaluated value of the cell.
        """
        return self.value

    def setValue(self, value):
        """
        Sets the evaluated value of the cell.
        """
        self.value = value
