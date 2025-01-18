from contentHandler.models.NumericalContent import NumericalContent
from contentHandler.models.FormulaContent import FormulaContent
from contentHandler.models.TextualContent import TextualContent
from contentHandler.models.TextualContent import Content

class Cell:
    """
    Represents a single cell within a spreadsheet.
    """

    def __init__(self, row: int, col: str, content, spreadsheet) -> None: #test
    def __init__(self, row: int, col: str, content, spreadsheet) -> None: #test
        """
        Initializes a cell with its coordinates and optional content.
        """
        #Content no es redundante? tenemos content como argumento y luego set content
        self.row = row
        self.col = col
        self.content = content  # Raw content of the cell (e.g., number, text, formula)
        self.value = self.content.getNumericalValue()  # Evaluated value of the cell (e.g., formula result)
        #print(f"Spreadsheet asociado: {spreadsheet}")
        self.spreadsheet = spreadsheet #test

        self.spreadsheet = spreadsheet #test

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
                print(f"Spreadsheet asociado en FormulaContent: {self.spreadsheet}")
                return FormulaContent(content[1:], self.spreadsheet) #test
            else:
                return TextualContent(content)
        except Exception as e:
            print(f"Error en la inicialización de Cell: {e}")
            raise

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

    def get_content(self) -> Content:
        """
        Gets the raw content of the cell.
        """
        return self.content

    def set_content(self, content):
        """
        Sets the raw content of the cell.
        """
        self.content = self._identify_content(content)
        self.value = self.content.getNumericalValue()

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
   
    def insertContent(self, content_string):
        """
        Inserts content into the cell, determining its type dynamically.

        :param content_string: A string representing the content to insert. It can be:
            - A formula (starts with '=').
            - A numerical value (integer or float).
            - A textual value (default).
        """
        # Elimina espacios en blanco al inicio y final
        content_string = content_string.strip()

        # Determina el tipo de contenido
        if content_string.startswith("="):
            # Es contenido de tipo formula
            formula_content = FormulaContent(content_string, self.spreadsheet)

            # Verifica dependencias circulares
            #self.checkCircularDependency(content_string) #test

            # Calcula la formula y actualiza dependencias
            formula_content.calculateFormula()
            #new_dependencies = formula_content.getCircularDependences() #test

            # Gestiona dependencias
            #self.updateDependencies(new_dependencies) #test

            # Establece el contenido
            self.content = formula_content

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


