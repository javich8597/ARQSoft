
class UserInterface:
    """
    Handles user proposals for creating, opening, closing, and saving spreadsheets,
    as well as additional commands defined in the requirements.
    """

    def __init__(self):
        """
        Initializes the user interface system.
        """
        self.options = {
            "RF": "Read commands from a file",
            "C": "Create a new spreadsheet",
            "E": "Edit a cell",
            "L": "Load a spreadsheet from a file",
            "S": "Save the spreadsheet to a file",
        }

    def displayMenu(self):
        """
        Prints the main menu options for the user.
        """
        print("\nMain Menu:")
        for key, description in self.options.items():
            print(f"{key}. {description}")

    def getUserChoice(self):
        """
        Gets the user choice from the menu.
        """
        choice = input("Enter your choice: ").strip()
        if choice.split()[0] not in self.options:  
            print("Invalid choice. Please try again.")
            return None
        return choice

#Print por la terminal toda la informacion de la celda