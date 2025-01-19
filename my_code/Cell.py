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
        content_string = str(content_string).strip() #ERROR

        # Determines the type of content
        if content_string.startswith("="):
            # Formula type
            formula_content = FormulaContent(content_string, self.spreadsheet)

            # Verifies circular dependencies (not implemented)
            #self.checkCircularDependency(content_string) #test

            # Calculate formula 
            formula_content.calculate_formula()

            #Find new dependencies (not implemented)
            #new_dependencies = formula_content.getCircularDependences() #test

            #Update dependencies (not implemented)
            #self.updateDependencies(new_dependencies) #test

            # Sets content and value
            self.content = formula_content #ERROR, DEBEMOS GUARDARLO EN VALUE, CONTENT TIENE QUE TENER FORMULA

        else:
            try:
                # Intenta convertir a numero (float)
                numeric_value = float(content_string)
                self.content = NumericalContent(numeric_value)

            except ValueError:
                # Si falla, asume que es texto
                self.content = TextualContent(content_string)

    def updateDependencies(self, new_dependencies):
        """
        Updates the dependencies of the cell based on the new dependencies provided.

        :param new_dependencies: A list of cell IDs that the current cell depends on.
        """
        old_dependencies = set(self.dependencies)
        self.dependencies = new_dependencies

        # Eliminar las dependencias que ya no existen
        for cell_id in old_dependencies - set(new_dependencies):
            self.spreadsheet.cells[cell_id].dependents.remove(self.cell_id)

        # Añadir nuevas dependencias
        for cell_id in new_dependencies:
            if self.cell_id not in self.spreadsheet.cells[cell_id].dependents:
                self.spreadsheet.cells[cell_id].dependents.append(self.cell_id)

    def checkCircularDependency(self, formula):
        """
        Verifies that adding the dependencies from the formula does not create a circular dependency.

        :param formula: The formula to analyze for dependencies.
        :raises CircularDependencyException: If a circular dependency is detected.
        """
        dependencies = self.extractDependenciesFromFormula(formula)
        visited = set()

        def dfs(cell_id):
            if cell_id in visited:
                raise CircularDependencyException(f"Circular dependency detected at {cell_id}")
            visited.add(cell_id)
            for dependent_cell in self.spreadsheet.cells[cell_id].dependencies:
                dfs(dependent_cell)

        for dependency in dependencies:
            dfs(dependency)

    def extractDependenciesFromFormula(self, formula):
        """
        Extracts cell references from the given formula.

        :param formula: The formula to parse.
        :return: A list of cell IDs (e.g., ['A1', 'B2']).
        """
        import re
        pattern = r"[A-Z]+[0-9]+"
        return re.findall(pattern, formula)

class CircularDependencyException(Exception):
    """
    Exception raised when a circular dependency is detected in the spreadsheet.
    """
    def __init__(self, message="Circular dependency detected"):
        super().__init__(message)


