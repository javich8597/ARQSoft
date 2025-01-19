from contentHandler.models.Content import Content
from my_code.FormulaManager.FormulaProcessing import computeFormula
from contentHandler.models.NumericalContent import NumericalContent
import re

class FormulaContent(Content):
    def __init__(self, formula: str, spreadsheet) -> None:
        super().__init__('formula', formula)
        self.formula = formula
        self.spreadsheet = spreadsheet
        

    def calculate_formula(self):
        try:

            cell_values = self.spreadsheet.get_cells() 
            formula = self.formula
            # Search for cell references in the formula and replace them with their values
            formula = self.process_references_cells(formula)

            #Search for functions in the formula and replace them with their results
            formula = self.process_functions_formula(formula)
            
            # Calculate the formula
            result = computeFormula(formula, cell_values)
            self.textualvalue = str(result)

            return result
        except Exception as e:
            print(f"Error in formula calculation: {e}")
            self.textualvalue = None
            return None

    def get_textual_value(self):
        return self.get_value()

    def get_content(self):
        return f"Formula: {self.formula}"

    def get_number_value(self):
        return self.calculate_formula()
        
    def process_functions_formula(self, formula: str):
        """
        Processes a formula by searching for functions and replacing them with their results in the same string.
        Process nested functions by evaluating them inside out.
        param formula: The formula in string format.
        return: The formula with the functions replaced by the results.
        """
        # Pattern to find functions in the formula
        function_pattern = re.compile(r"(\w+)\(([^()]*?)\)")  # Includes anidated functions
        
        while True:
            # Find anidated functions in the formula
            matches = list(function_pattern.finditer(formula))
            if not matches:
                break 
            
            # Process each function in reverse order
            for match in reversed(matches):
                function_name, args_str = match.groups()
                
                # Process arguments
                args = []
                for arg in args_str.split(";"):
                    arg = arg.strip()
                    if ":" in arg:  
                        arg = self.process_references_cells(arg)  
                    args.append(arg)
                
                # Convert arguments to numbers
                numeric_args = [float(arg) for arg in ";".join(args).split(";")]
                
                # Evaluate the function
                result = self.evaluate_function(function_name, numeric_args)
                
                # Replace the function with the result
                formula = (
                    formula[:match.start()] +
                    str(result) +
                    formula[match.end():]
                )
        
        return formula

   
    def process_references_cells(self, formula: str):
        # Process cell ranges
        cellValues = self.spreadsheet.get_cells() 
        range_pattern = r"([A-Z]+[0-9]+):([A-Z]+[0-9]+)"
        for match in re.finditer(range_pattern, formula):
            coord1, coord2 = match.groups()  # Coordinates of the range
            cell_range = self.get_cell_range(coord1, coord2)  # Get all cells in the range
            if not cell_range:
                raise ValueError(f"Invalid range: {coord1}:{coord2}")

            # Replace the range with the values of the cells
            values = []
            for cell_coord in cell_range:
                if cell_coord in cellValues and isinstance(cellValues[cell_coord], NumericalContent):
                    values.append(str(cellValues[cell_coord].get_number_value()))
                else:
                    raise ValueError(f"Cell {cell_coord} in range {coord1}:{coord2} is undefined or invalid.")
            
            # Build the replacement string
            replacement = ";".join(values)
            formula = formula.replace(f"{coord1}:{coord2}", replacement)

        # Process individual cell references
        pattern = r"\b[A-Z]+[0-9]+\b" 
        def replace_reference(match):
            ref = match.group(0)
            if ref in cellValues and isinstance(cellValues[ref], NumericalContent):
                return str(cellValues[ref].get_number_value())
            else:
                raise ValueError(f"Undefined or invalid cell reference: {ref}")

        # Replace cell references in the formula
        formula = re.sub(pattern, replace_reference, formula)

        return formula

  
    def get_referenced_cells(content):
        """
        Extracts cell references (e.g., 'A2', 'A3') from the formula.
        """
        pattern = r"[A-Z]+[0-9]+"
        return re.findall(pattern, content)  


    def evaluate_function(self,function_name, args):
        """
        Simulates the evaluation of a function (e.g. SUM, MIN).
        param function_name: Name of the function to evaluate.
        :param args: List of arguments to the function.
        return: The result of the function.
        """
        if function_name == "SUMA":
            return sum(args)
        elif function_name == "MIN":
            return min(args)
        elif function_name == "MAX":
            return max(args)
        elif function_name == "PROMEDIO":
            return sum(args) / len(args)
        else:
            raise ValueError(f"Function {function_name} not supported.")


    def get_cell_range(self, coord1: str, coord2: str):
            """
            Returns a list of cell coordinates within a rectangular range.
            
            :param coord1: The top-left cell of the range (e.g., "A1").
            :param coord2: The bottom-right cell of the range (e.g., "B2").
            :return: A list of cell coordinates (e.g., ["A1", "A2", "B1", "B2"]).
            """
            # Extract column and row from coordinates
            col1, row1 = re.match(r"([A-Z]+)([0-9]+)", coord1).groups()
            col2, row2 = re.match(r"([A-Z]+)([0-9]+)", coord2).groups()

            # Convert rows to integers
            row1, row2 = int(row1), int(row2)

            # Reorder coordinates
            col_start, col_end = sorted([col1, col2])
            row_start, row_end = sorted([row1, row2])

            # Generate a list of columns within the range
            def generate_columns(start_col, end_col):
                cols = []
                current = start_col
                while current <= end_col:
                    cols.append(current)
                    current = increment_column(current)
                return cols

            # Increase column (e.g., "A" → "B", "Z" → "AA")
            def increment_column(col):
                col = list(col)
                i = len(col) - 1
                while i >= 0:
                    if col[i] == 'Z':
                        col[i] = 'A'
                        i -= 1
                        if i < 0:
                            col.insert(0, 'A')
                    else:
                        col[i] = chr(ord(col[i]) + 1)
                        break
                return ''.join(col)

            # Generate columns and rows within the range
            columns = generate_columns(col_start, col_end)
            coord_list = [f"{col}{row}" for col in columns for row in range(row_start, row_end + 1)]

            return coord_list

