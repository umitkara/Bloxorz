from typing import List
import heapq

EMPTY = '1'
WALL = '0'
START = 'B'
END = 'X'

class Node:
    def __init__(self,parent:'Node', node_type:str, x1:int, y1:int, x2:int, y2:int, direction:str=''):
        self.parent = parent
        self.node_type = node_type
        self.g = 0
        self.h = 0
        self.f = 0
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.visited = False
        self.direction = direction
    def get_positions(self) -> tuple:
        return (self.x1, self.y1, self.x2, self.y2)
    def __eq__(self, other):
        if type(other) is Node:
            return self.x1 == other.x1 and self.y1 == other.y1 and self.x2 == other.x2 and self.y2 == other.y2
        elif type(other) is tuple:
            return self.x1 == other[0] and self.y1 == other[1] and self.x2 == other[2] and self.y2 == other[3]
        else:
            return False
    def __lt__(self, other:'Node'):
        return self.f < other.f
    
def aStar(start:Node, end:Node, grid:List[List[str]]) -> List[tuple]:
    open_list = []
    closed_list = []
    heapq.heappush(open_list, start)
    while open_list:
        current:Node = heapq.heappop(open_list)
        if current == end:
            return reconstruct_path(current)
        closed_list.append(current)
        for neighbor in get_neighbors(current, grid):
            if neighbor not in closed_list:
                neighbor.g = current.g + 1
                neighbor.h = get_heuristic(neighbor, end)
                neighbor.f = neighbor.g + neighbor.h
                if neighbor not in open_list:
                    heapq.heappush(open_list, neighbor)
    return []

def reconstruct_path(current:Node) -> List[tuple]:
    path = []
    while current.parent is not None:
        path.append(current.direction)
        current = current.parent
    return ''.join(path[::-1])

def get_heuristic(current:Node, end:Node) -> int:
    return 1/4 * max(max(abs(current.x1 - end.x1), abs(current.y1 - end.y1)), max(abs(current.x2 - end.x2), abs(current.y2 - end.y2)))

def get_neighbors(current:Node, grid:List[List[str]]) -> List[Node]:
    if current.x1 == current.x2 and current.y1 == current.y2:
        return get_standing(current, grid)
    elif current.x1 != current.x2 and current.y1 == current.y2:
        return get_lying_x(current, grid)
    elif current.x1 == current.x2:
        return get_lying_y(current, grid)

def get_standing(current:Node, grid:List[List[str]]) -> List[Node]:
    neighbors = []
    X, Y = current.x1, current.y1
    if X > 1 and grid[Y][X-1] != WALL and grid[Y][X-2] != WALL:
        neighbors.append(Node(current, EMPTY, X-2, Y, X-1, Y, 'L'))
    if X < len(grid[0])-2 and grid[Y][X+1] != WALL and grid[Y][X+2] != WALL:
        neighbors.append(Node(current, EMPTY, X+1, Y, X+2, Y, 'R'))
    if Y > 1 and grid[Y-1][X] != WALL and grid[Y-2][X] != WALL:
        neighbors.append(Node(current, EMPTY, X, Y-2, X, Y-1, 'U'))
    if Y < len(grid)-2 and grid[Y+1][X] != WALL and grid[Y+2][X] != WALL:
        neighbors.append(Node(current, EMPTY, X, Y+1, X, Y+2, 'D'))
    return neighbors

def get_lying_x(current:Node, grid:List[List[str]]) -> List[Node]:
    neighbors = []
    X1, Y1, X2, Y2 = current.get_positions()
    if X1 > 0 and grid[Y1][X1-1] != WALL:
        neighbors.append(Node(current, EMPTY, X1-1, Y1, X2-2, Y2, 'L'))
    if X2 < len(grid[0])-1 and grid[Y1][X2+1] != WALL:
        neighbors.append(Node(current, EMPTY, X1+2, Y1, X2+1, Y2, 'R'))
    if Y1 > 0 and grid[Y1-1][X1] != WALL and grid[Y2-1][X2] != WALL:
        neighbors.append(Node(current, EMPTY, X1, Y1-1, X2, Y2-1, 'U'))
    if Y2 < len(grid)-1 and grid[Y1+1][X1] != WALL and grid[Y1+1][X2] != WALL:
        neighbors.append(Node(current, EMPTY, X1, Y1+1, X2, Y2+1, 'D'))
    return neighbors

def get_lying_y(current:Node, grid:List[List[str]]) -> List[Node]:
    neighbors = []
    X1, Y1, X2, Y2 = current.get_positions()
    if Y1 > 0 and grid[Y1-1][X1] != WALL:
        neighbors.append(Node(current, EMPTY, X1, Y1-1, X2, Y2-2, 'U'))
    if Y2 < len(grid)-1 and grid[Y2+1][X1] != WALL:
        neighbors.append(Node(current, EMPTY, X1, Y1+2, X2, Y2+1, 'D'))
    if X1 > 0 and grid[Y1][X1-1] != WALL and grid[Y2][X2-1] != WALL:
        neighbors.append(Node(current, EMPTY, X1-1, Y1, X2-1, Y2, 'L'))
    if X2 < len(grid[0])-1 and grid[Y1][X2+1] != WALL and grid[Y2][X2+1] != WALL:
        neighbors.append(Node(current, EMPTY, X1+1, Y1, X2+1, Y2, 'R'))
    return neighbors

if __name__ == "__main__":
    maze = ['00011111110000',
            '00011111110000',
            '11110000011100',
            '11100000001100',
            '11100000001100',
            '1B100111111111',
            '11100111111111',
            '000001X1001111',
            '00000111001111']

    start, end = None,None

    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == START:
                start = Node(None, START, x, y, x, y)
            elif maze[y][x] == END:
                end = Node(None, END, x, y, x, y)
    print(aStar(start, end, maze))