from my_code.Spreadsheet import Spreadsheet

class DependencyManager:
    """
    Manages cell dependencies and ensures no circular references exist.
    """

    def __init__(self):
        """
        Initializes the dependency manager with an empty dependency graph.
        """
        self.dependency_graph = {}
        self.Spreadsheet = Spreadsheet()


    def addDependency(self, cell: str, dependencies: list):
        """
        Adds a dependency for a specific cell.

        :param cell: The cell to add dependencies for.
        :param dependencies: A list of cells that the specified cell depends on.
        """
        if cell not in self.dependency_graph:
            self.dependency_graph[cell] = set()
        self.dependency_graph[cell].update(dependencies)

    def removeDependency(self, cell: str):
        """
        Removes a cell and its dependencies from the graph.

        :param cell: The cell to remove from the dependency graph.
        """
        if cell in self.dependency_graph:
            del self.dependency_graph[cell]
        for deps in self.dependency_graph.values():
            deps.discard(cell)

    def checkDependencies(self, cell: str) -> bool:
        """
        Checks for circular dependencies starting from a given cell.

        :param cell: The starting cell to check for circular dependencies.
        :return: True if no circular dependency exists, False otherwise.

        Exceptional Situations:
            - CircularDependencyException: Raised if a circular dependency is detected.
        """
        visited = set()
        stack = set()

        def visit(node):
            if node in stack:
                raise CircularDependencyException(f"Circular dependency detected involving cell {node}.")
            if node not in visited:
                visited.add(node)
                stack.add(node)
                for neighbor in self.dependency_graph.get(node, []):
                    visit(neighbor)
                stack.remove(node)

        try:
            visit(cell)
            return True
        except CircularDependencyException as e:
            print(e)
            return False
        
    def getCellValues(self):
        return self.Spreadsheet.getCellValues()

class CircularDependencyException(Exception):
    """
    Exception raised when a circular dependency is detected.
    """
    pass
