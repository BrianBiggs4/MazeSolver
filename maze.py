from enum import Enum
from typing import List, NamedTuple, Callable, Optional
import random
from math import sqrt
from search_algorithms import dfs, node_to_path, bfs, astar

class Cell(str, Enum):
    EMPTY = ' '
    BLOCKED = 'X'
    START = 'S'
    GOAL = 'G'
    PATH = '*'

class MazeLocation(NamedTuple):
    row: int
    column: int
  
class Maze:
    def __init__(self, rows: int = 10, columns: int = 10, sparseness: float = 0.2, start: MazeLocation = MazeLocation(0,0), goal: MazeLocation = MazeLocation(9, 9)) -> None:
        self._rows = rows
        self._columns = columns
        self.start = start
        self.goal = goal

        # Filling the grid with empty cells
        self._grid = [[Cell.EMPTY for c in range(columns)] for r in range(rows)]

        # Populating the grid with blocked cells
        self._randomly_fill(rows, columns, sparseness)
        
        # Fill the start and goal locations in
        self._grid[start.row][start.column] = Cell.START
        self._grid[goal.row][goal.column] = Cell.GOAL
    
    def _randomly_fill(self, rows: int, columns: int, sparseness: float):
        for row in range(rows):
            for column in range(columns):
                if random.uniform(0, 1.0) < sparseness:
                    self._grid[row][column] = Cell.BLOCKED

    # return a nice formatted version of the maze for printing.
    def __str__(self):
        output = ''
        for row in self._grid:
            output += ''.join([c.value for c in row ]) + '\n'
        return output 
    
    # Return True or False if MazeLocation found the goal
    def goal_test(self, ml: MazeLocation) -> bool:
        return ml == self.goal

    # Find possible next locations from a given MazeLocation.
    def successors(self, ml: MazeLocation) -> List[MazeLocation]:
        locations = []
        if ml.row + 1 < self._rows and self._grid[ml.row + 1][ml.column] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row + 1, ml.column))

        if ml.row - 1 >= 0 and self._grid[ml.row - 1][ml.column] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row - 1, ml.column))

        if ml.column + 1 < self._columns and self._grid[ml.row][ml.column + 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column + 1))

        if ml.column - 1 >= 0 and self._grid[ml.row][ml.column - 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column - 1))
        return locations

    def mark(self, path: List[MazeLocation]):
        for maze_location in path:
            self._grid[maze_location.row][maze_location.column] = Cell.PATH
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL
    
    def clear(self, path: List[MazeLocation]):
        for maze_location in path:
            self._grid[maze_location.row][maze_location.column] = Cell.EMPTY
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL

# Length of of a straight line from the starting point to the goal - pythagorean theorem
def euclidean_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    def distance(ml: MazeLocation) -> float:
        xdist = ml.column - goal.column
        ydist = ml.row - goal.row
        return sqrt((xdist * xdist) + (ydist * ydist))
    return distance

# Derived by finding the difference in rwos between to maze locations and summing it witht he difference in columns
def manhattan_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    def distance(ml: MazeLocation) -> float:
        xdist = abs(ml.column - goal.column)
        ydist = abs(ml.row - goal.row)
        return (xdist + ydist)
    return distance


if __name__ == '__main__':
    print("Here is the maze! \n")
    m = Maze()
    print(m)

    # Test DFS
    print("Here is the DFS search algorithm \n")
    solution1 = dfs(m.start, m.goal_test, m.successors)
    if solution1 is None:
        print("No solution found using DFS")
    else:
        path1 = node_to_path(solution1)
        m.mark(path1)
        print(m)
        m.clear(path1)

    # Test DFS
    print("Here is the BFS search algorithm \n")
    solution2 = bfs(m.start, m.goal_test, m.successors)
    if solution2 is None:
        print("No solution found for BFS")
    else:
        path2 = node_to_path(solution2)
        m.mark(path2)
        print(m)
        m.clear(path2)

    # Test A*
    print("Here is the A* algorithm \n")
    distance = manhattan_distance(m.goal)
    solution3 = astar(m.start, m.goal_test, m.successors, distance)
    if solution3 is None:
        print("No solution found using A*")
    else:
        path3 = node_to_path(solution3)
        m.mark(path3)
        print(m)