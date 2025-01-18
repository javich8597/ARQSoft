
class DependencyManager:
    """
    Manages dependencies between cells in a spreadsheet.
    """
    def __init__(self):
        # Diccionario que mapea cada celda a sus dependencias
        self.dependencies = {}

    def addDependencies(self, cell_id, dependent_ids):
        """
        Adds dependencies for a given cell.

        :param cell_id: The cell that has dependencies.
        :param dependent_ids: A list of cells that the cell depends on.
        """
        if cell_id not in self.dependencies:
            self.dependencies[cell_id] = set()

        for dep_id in dependent_ids:
            self.checkCircularDependency(cell_id, dep_id)
            self.dependencies[cell_id].add(dep_id)

    def removeDependencies(self, cell_id):
        """
        Removes all dependencies for a given cell.

        :param cell_id: The cell whose dependencies should be removed.
        """
        if cell_id in self.dependencies:
            del self.dependencies[cell_id]

    def getDependents(self, cell_id):
        """
        Returns a list of cells that depend on the given cell.

        :param cell_id: The cell to check dependents for.
        :return: A list of dependent cell IDs.
        """
        dependents = []
        for dependent, deps in self.dependencies.items():
            if cell_id in deps:
                dependents.append(dependent)
        return dependents

    def checkCircularDependency(self, start_cell, target_cell):
        """
        Checks if adding a dependency creates a circular dependency.

        :param start_cell: The cell to check from.
        :param target_cell: The cell to check to.
        :raises CircularDependencyException: If a circular dependency is detected.
        """
        visited = set()

        def dfs(cell_id):
            if cell_id in visited:
                raise CircularDependencyException(f"Circular dependency detected: {cell_id}")
            visited.add(cell_id)
            for dep in self.dependencies.get(cell_id, []):
                dfs(dep)

        dfs(target_cell)

class CircularDependencyException(Exception):
    """
    Exception raised when a circular dependency is detected.
    """
    pass
