from Controllers.SpreadsheetController import SpreadsheetController

if _name_ == "_main_":
    spreadsheetcontroller = SpreadsheetController()
    while True:
        
        try:
            spreadsheetcontroller.showMenu()
        except Exception as Error:
            print(Error.message)
