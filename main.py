import os

from Controllers.SpreadsheetController import SpreadsheetController


def main():
    spreadsheetcontroller = SpreadsheetController()
    while True:
        try:
            spreadsheetcontroller.showMenu()
        except Exception as Error:
            print(Error.message)

if __name__ == "__main__":
    main()
