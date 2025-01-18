from my_code.Spreadsheet import Spreadsheet
class SpreadsheetSaver:
    @staticmethod
    def save_spreadsheet(file_path: str, spreadsheet: Spreadsheet):

        try:
            with open(file_path, 'w') as file:
                #for coord, cell in spreadsheet.getCells().items():
                    #value = cell.getValue()
                    #if value is not None:
                        #file.write(f"{value}\n")
                for coord, cell in spreadsheet.cells.items():
                    file.write(f"{coord}: {cell.get_content()}\n")
        except Exception as e:
            raise RuntimeError(f"An error occurred while saving the file: {e}")

    @staticmethod
    def is_valid_path(filepath):
        import os
        return os.path.isdir(os.path.dirname(filepath)) or os.path.isfile(filepath)

    @staticmethod
    def if_file_exists(filepath):
        import os
        return os.path.exists(filepath)
