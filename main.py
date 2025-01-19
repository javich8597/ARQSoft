import os

from controllers.SpreadsheetController import SpreadsheetController


def main():
    spreadsheetcontroller = SpreadsheetController()
    while True:
        try:
            spreadsheetcontroller.show_menu()
        except Exception as error:
            print(f"Error: {error}")

if __name__ == "__main__":
    main()
