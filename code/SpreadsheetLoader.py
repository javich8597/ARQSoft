class SpreadsheetLoader:
    @staticmethod
    def load_spreadsheet(path):
        try:
            with open(path, "r") as file:
                data = file.read()
                return SpreadsheetLoader.parse_s2v_format(data)
        except FileNotFoundError:
            raise FileNotFoundError("The specified file was not found.")
        except Exception as e:
            raise RuntimeError(f"An error occurred while loading the file: {e}")

    @staticmethod
    def parse_s2v_format(data):
        spreadsheet = Spreadsheet()
        try:
            lines = data.splitlines()
            for line in lines:
                coordinate, content = line.split(":")
                spreadsheet.set_cell_content(coordinate.strip(), content.strip())
            return spreadsheet
        except Exception:
            raise ValueError("The file format is invalid. Unable to parse S2V format.")
