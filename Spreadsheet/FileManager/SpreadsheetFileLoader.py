class SpreadsheetFileLoader:
    def __init__(self, spreadsheet):
        self.spreadsheet = spreadsheet

    def load(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                position, content = line.strip().split(': ')
                # Aquí deberías crear una instancia de Cell con el contenido adecuado
                # y agregarla a la hoja de cálculo
                # cell = Cell(position, Content(content))
                # self.spreadsheet.add_cell(cell)
        print(f"Hoja de cálculo cargada desde {file_path}")
