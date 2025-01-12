class UserInterface:
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
            "5": "Exit"
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
        if choice not in self.options:
            print("Invalid choice. Please try again.")
            return None
        return choice

    def readCommandsFromFile(self, file_path: str):
        """
        Reads and processes commands from a file.
        """
        try:
            with open(file_path, "r") as file:
                for line in file:
                    print(f"Processing command: {line.strip()}")
                    self.processCommand(line.strip())
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}.")

    def createSpreadsheet(self):
        """
        Creates a new empty spreadsheet.
        """
        print("Creating a new spreadsheet...")
        # Logic for creating a new spreadsheet.

    def editCell(self, coordinate: str, content: str):
        """
        Edits the content of a specified cell.
        """
        print(f"Editing cell {coordinate} with new content: {content}")
        # Logic for editing a cell.

    def loadSpreadsheet(self, path: str):
        """
        Loads a spreadsheet from a file.
        """
        print(f"Loading spreadsheet from {path}...")
        # Logic for loading a spreadsheet.

    def saveSpreadsheet(self, path: str):
        """
        Saves the spreadsheet to a file.
        """
        print(f"Saving spreadsheet to {path}...")
        # Logic for saving a spreadsheet.

    def processCommand(self, command: str):
        """
        Processes a single command entered by the user or read from a file.
        """
        parts = command.split(maxsplit=2)
        cmd = parts[0]

        if cmd == "RF":
            if len(parts) < 2:
                print("Error: Missing file path for RF command.")
            else:
                self.readCommandsFromFile(parts[1])
        elif cmd == "C":
            self.createSpreadsheet()
        elif cmd == "E":
            if len(parts) < 3:
                print("Error: Missing arguments for E command.")
            else:
                self.editCell(parts[1], parts[2])
        elif cmd == "L":
            if len(parts) < 2:
                print("Error: Missing file path for L command.")
            else:
                self.loadSpreadsheet(parts[1])
        elif cmd == "S":
            if len(parts) < 2:
                print("Error: Missing file path for S command.")
            else:
                self.saveSpreadsheet(parts[1])
        else:
            print(f"Error: Unknown command {cmd}.")

    def run(self):
        """
        Main loop for interacting with the user.
        """
        while True:
            self.displayMenu()
            choice = input("Enter your command: ").strip()
            if choice == "5":
                print("Exiting the program. Goodbye!")
                break
            self.processCommand(choice)
