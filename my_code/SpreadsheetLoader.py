from my_code.Spreadsheet import Spreadsheet
from pathlib import Path
import sys

class SpreadsheetLoader:
    @staticmethod
    def __resolve_file_path(file_path: str) -> Path:
        """Solver for relative paths"""
        file_path = Path(file_path)

        # path absolute
        if file_path.is_absolute():
            return file_path.resolve()

        # This is relative path to the current working directory
        entry_script_path = Path(sys.argv[0]).resolve()
        script_parent_dir = entry_script_path.parent
        resolved_path = (script_parent_dir / file_path).resolve()

        return resolved_path

    @staticmethod
    def load_spreadsheet(path):
        resolved_path = SpreadsheetLoader.__resolve_file_path(path)
        try:
            with open(resolved_path, "r") as file:
                data = file.read()
                return SpreadsheetLoader.parse_s2v_format(data)
        except FileNotFoundError:
            raise FileNotFoundError(f"The specified file was not found: {resolved_path}")
        except Exception as e:
            raise RuntimeError(f"An error occurred while loading the file: {e}")

    @staticmethod
    def parse_s2v_format(data):
        spreadsheet = Spreadsheet()
        try:
            lines = data.splitlines()
            for row_index, line in enumerate(lines, start=1):
                cells = line.split(";")
                for col_index, content in enumerate(cells, start=1):
                    if content.strip():
                        if "(" in content and "," in content:
                            content = content.replace(",", ";")
                        coordinate = f"{chr(64 + col_index)}{row_index}"
                        spreadsheet.set_cell_content(coordinate, content.strip())
            return spreadsheet
        except Exception:
            raise ValueError("The file format is invalid. Unable to parse S2V format.")
