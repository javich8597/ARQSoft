class Spreadsheet:
    def __init__(self):
        self.cells = {}

    def add_cell(self, cell):
        self.cells[cell.position] = cell

    def get_cell(self, position):
        return self.cells.get(position, None)

    def display(self):
        for position, cell in self.cells.items():
            print(f"{position}: {cell.get_content()}")
