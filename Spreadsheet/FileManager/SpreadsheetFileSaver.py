class SpreadsheetFileSaver:
    def __init__(self, spreadsheet):
        self.spreadsheet = spreadsheet

    def save(self, file_path):
        with open(file_path, 'w') as file:
            for position, cell in self.spreadsheet.cells.items():
                file.write(f"{position}: {cell.get_content()}\n")
        print(f"Hoja de cálculo guardada en {file_path}")
