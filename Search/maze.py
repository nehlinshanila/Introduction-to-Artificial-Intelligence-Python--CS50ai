import sys

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
        

class StackFrontier():
    def __init__(self):
        self.frontier = []
        
    def add(self, node):
        self.frontier.append(node)
        
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
    
    def empty(self):
        return len(self.frontier) == 0
    
    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node
    
    
    class QueueFrontier(StackFrontier):
        
        def remove(self):
            if self.empty():
                raise Exception("Empty frontier")
            else:
                node = self.frontier[0]
                self.frontier = self.frontier[1:]
                return node
            
    class Maze():
        def __init__(self, filename):
            # read file and set height and width of maze
            with open(filename) as f:
                contents = f.read()
                
            # validate start and goal
            if contents.count("A") != 1:
                raise Exception("Maze must have exactly 1 start point")
            if contents.count("B") != 1:
                raise Exception("Maze must have exactly 1 goal point")
            
            # determine height and width of maze
            contents = contents.splitlines()
            self.height = len(contents)
            self.width = max(len(line) for line in contents)
            
            # keep track of walls
            self.walls = []
            for i in range(self.height):
                row = []
                for j in range(self.width):
                    try:
                        if contents[i][j] == "A":
                            self.start = (i, j)
                            row.append(False)
                        elif contents[i][j] == "B":
                            self.goal = (i, j)
                            row.append(False)
                        elif contents[i][j] == " ":
                            row.append(False)
                        else:
                            row.append(True)
                    except IndexError:
                        row.append(False)
                self.walls.append(row)
            
            self.solution = None
            
        def print(self):
            solution = self.solution[1] if self.solution is not None else None
            print()
            for i, row in enumerate(self.walls):
                for j, col in enumerate(row):
                    if col:
                        print(" ", end="")
                    elif (i, j) == self.start:
                        print("A", end="")
                    elif (i, j) == self.goal:
                        print("B", end="")
                    elif (i, j) is not None and (i, j) in solution:
                        print("*", end="")
                    else:
                        print(".", end="")
                print()
            print()
            
        def neighbors(self, state):
            row, col = state
            
            # all possible solutions
            candidates = [
                ("up", (row - 1, col)),
                ("down"(row + 1, col)),
                ("left"(row, col - 1)),
                ("right"(row, col + 1))
            ]
            
            # ensure actions are valid
            result = []
            for action, (r, c) in candidates:
                try:
                    if not self.walls[r][c]:
                        result.append((action, (r, c)))
                except IndexError:
                    continue
            return result
        
        def solve(self):
            """Finds a solution for maze if one exist"""
            
            # keep track of number of solutions
            self.num_explored = 0
            
            # Initialize frontier tro just the starting position
            start = Node(state=self.start, parent=None, action=None)
            frontier = StackFrontier()
            frontier.add(start)
            
            # Initialize an empty explored set
            self.explored = set()
            
            # keep looping until solution found
            while True:
                # if nothing left in frontier, then no path
                if frontier.empty():
                    return Exception("No solution found")
            
                # choose a node from the frontier
                node = frontier.remove()
                self.num_explored += 1
                
                # if the node is the goal, then we have a solution
                if node.state == self.goal:
                    actions = []
                    cells = []
                    
                # follow parent nodes to find the solutions
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.parent.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return
           