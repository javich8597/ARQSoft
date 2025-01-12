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
        self.content = content  # Raw content of the cell (e.g., number, text, formula)
        self.value = None  # Evaluated value of the cell (e.g., formula result)

    def getCoordinate(self):
        """
        Returns the coordinates of the cell as a tuple (row, col).
        """
        return self.row, self.col

    def setCoordinate(self, row: int, col: str):
        """
        Sets the coordinates of the cell composed by row and column.
        """
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
        self.content = content

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
