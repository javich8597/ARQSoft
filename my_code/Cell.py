from contentHandler.models.NumericalContent import NumericalContent
from contentHandler.models.FormulaContent import FormulaContent
from contentHandler.models.TextualContent import TextualContent
from contentHandler.models.TextualContent import Content


class Cell:
    """
    Represents a single cell within a spreadsheet.
    """

    def __init__(self, row: int, col: str, content, spreadsheet) -> None: 
        """
        Initializes a cell with its coordinates and optional content.
        """
        self.row = row
        self.col = col
        self.content = content  # Raw content of the cell (e.g., number, text, formula)
        self.value = None  # Evaluated value of the cell (e.g., formula result) 
        self.spreadsheet = spreadsheet 

    def _identify_content(self, content):
        try:
            """
            Identifies the type of content and returns the appropriate content object.
            """
            if content is None:
                return None
            if isinstance(content, (int, float)):
                return NumericalContent(content)
            elif isinstance(content, str) and content.startswith("="):
                return FormulaContent(content[1:], self.spreadsheet) #test
            else:
                return TextualContent(content)
        except Exception as e:
            print(f"Error in Cell identification: {e}")
            raise

    def get_content(self) -> Content:
        """
        Gets the raw content of the cell.
        """
        return self.content

    def get_value(self):
        """
        Returns the evaluated value of the cell.
        """
        return self.value
   
    def insert_content(self, content_string):
        """
        Inserts content into the cell, determining its type dynamically.

        :param content_string: A string representing the content to insert. It can be:
            - A formula (starts with '=').
            - A numerical value (integer or float).
            - A textual value (default).
        """
        # Deletes spaces at the beginning and end of the string
        content_string = str(content_string).strip() 

        # Determines the type of content
        if content_string.startswith("="):
            # Set to formula content
            formula_content = FormulaContent(content_string, self.spreadsheet)

            # Calculate formula 
            formula_content.calculate_formula()

            # Sets content and value
            self.content = formula_content 
            self.value = formula_content.get_textual_value() 

        else:
            try:
                # Try to convert to number (float)
                numeric_value = float(content_string)
                self.content = NumericalContent(numeric_value)

            except ValueError:
                # If fails is text
                self.content = TextualContent(content_string)
