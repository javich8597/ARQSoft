class SpreadsheetSaver:
    @staticmethod
    def save_spreadsheet(path, spreadsheet):
        try:
            with open(path, "w") as file:
                for coord, cell in spreadsheet.cells.items():
                    file.write(f"{coord}: {cell.get_content().getValue()}\n")
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
