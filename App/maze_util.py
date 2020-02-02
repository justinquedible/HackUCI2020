
import numpy as np
from random import randint
import queue
class Maze:
    def __init__(self, x,y,z):
        self.xMax = x
        self.yMax = y
        self.zMax = z
        self.grid = initGrid(x,y,z)
    
    def getLevel(self, index):
        if index < self.zMax+1:
            return self.grid[index]
        else:
            raise IndexError

def isSquare(src, dest, grid):
    sx, sy , sz = src
    dx, dy, dz = dest

    #Potential squares, we explicitly disallow square patterns in the grid.
    if dx + 1 < len(grid) and dy > 0 and (grid[dx+1][dy][dz] + grid[dx+1][dy-1][dz] + grid[dx][dy-1][dz] == 3): #NE
        return True
    elif dx > 0 and dy > 0 and (grid[dx-1][dy][dz] + grid[dx-1][dy-1][dz] + grid[dx][dy-1][dz] == 3): #NW
        return True
    elif dx + 1 < len(grid) and dy + 1 < len(grid[0]) and (grid[dx+1][dy][dz] + grid[dx+1][dy+1][dz] + grid[dx][dy+1][dz] == 3): #SE
        return True
    elif dx > 0 and dy + 1 < len(grid[0]) and (grid[dx-1][dy][dz] + grid[dx-1][dy+1][dz] + grid[dx][dy+1][dz] == 3): #SW
        return True
    elif dz + 1 < len(grid[0][0]) and dy > 0 and (grid[dx][dy][dz+1] + grid[dx][dy-1][dz+1] + grid[dx][dy-1][dz] == 3): #N - Up
        return True
    elif dz > 0 and dy > 0 and (grid[dx][dy][dz-1] + grid[dx][dy-1][dz-1] + grid[dx][dy-1][dz] == 3): #N - Down
        return True
    elif dz + 1 < len(grid[0][0]) and dy+1 < len(grid[0]) and (grid[dx][dy][dz+1] + grid[dx][dy+1][dz+1] + grid[dx][dy+1][dz] == 3): #S - Up
        return True
    elif dz > 0 and dy+1 < len(grid[0]) and (grid[dx][dy][dz-1] + grid[dx][dy+1][dz-1] + grid[dx][dy+1][dz] == 3): #S - Down
        return True
    elif dx + 1 < len(grid) and dz + 1 < len(grid[0][0]) and (grid[dx][dy][dz+1] + grid[dx+1][dy][dz+1] + grid[dx+1][dy][dz] == 3): #E - Up
        return True
    elif dx + 1 < len(grid) and dz  > 0  and (grid[dx][dy][dz-1] + grid[dx+1][dy][dz-1] + grid[dx+1][dy][dz] == 3): #E - Down
        return True
    elif dx > 0 and dz + 1 < len(grid[0][0]) and (grid[dx][dy][dz+1] + grid[dx-1][dy][dz+1] + grid[dx-1][dy][dz] == 3 ): #W - Up
        return True
    elif dx > 0 and dz > 0 and (grid[dx][dy][dz-1] + grid[dx-1][dy][dz-1] + grid[dx-1][dy][dz] == 3): #W - Down
        return True
    else:
        return False

def getAdj(cell, grid, visited):
    adj = list()
    x, y, z = cell

    #Potential neighbours
    east = (x+1, y, z)
    west = (x-1, y, z)
    north = (x, y-1, z)
    south = (x, y+1, z)
    up = (x,y,z + 1)
    down = (x, y, z-1)

    #Add qualifying neighbours to list of adjacent
    if x + 1 < len(grid) and east not in visited and not isSquare(cell, east, grid):
        adj.append(east)
    if y + 1 < len(grid) and south not in visited and not isSquare(cell, south, grid):
        adj.append(south) 
    if x > 0 and west not in visited and not isSquare(cell, west, grid):
        adj.append(west) 
    if y > 0 and north not in visited and not isSquare(cell, north, grid):
        adj.append(north) 
    if z + 1 < len(grid) and up not in visited and not isSquare(cell, up, grid):
        adj.append(up) 
    if z > 0 and down not in visited and not isSquare(cell, down, grid):
        adj.append(down) 
    return adj

def initGrid(xMax, yMax, zMax):
    grid = np.zeros(shape=(xMax,yMax,yMax), dtype = np.int8)

    toVisit = list() #The stack of cells to visit
    visited = set()  #Set of cells that have been visited already
    start = (0, 0, 0)
    visited.add(start)
    toVisit.append(start)
    grid[start[0]][start[1]][start[2]] = 1

    while len(toVisit) != 0:
        cell = toVisit.pop()
        adjN = getAdj(cell, grid, visited)

        #The current cell has some unvisited neighbour
        if len(adjN) != 0:
            toVisit.append(cell)
            other = adjN[randint(0, len(adjN)-1)]
            grid[other[0]][other[1]][other[2]] = 1
            visited.add(other)
            toVisit.append(other)


    #Mark vertical paths.
    # 3 - can go up from current cell
    # 4 - can go down from current cell
    # 5 - can go either up or down. 
    rand = 20
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            for k in range(len(grid[0][0])):
                if grid[i][j][k] > 0:
                    if i > 0 and i + 1 < len(grid) and grid[i-1][j][k] > 0 and grid[i+1][j][k] > 0 and randint(0,rand) == 0:
                        grid[i][j][k] = 5
                        if grid[i-1][j][k] == 1:
                            grid[i-1][j][k] = 3
                        if i < len(grid) and grid[i+1][j][k] == 1:
                            grid[i+1][j][k] = 4
                    elif i > 0 and grid[i-1][j][k] > 0 and randint(0,rand) == 0:
                        grid[i][j][k] = 4
                        if i > 0 and grid[i-1][j][k] == 1:
                            grid[i-1][j][k] = 3
                    elif i + 1 < len(grid) and grid[i+1][j][k] > 0 and randint(0,rand) == 0:
                        grid[i][j][k] = 3
                        if i < len(grid):
                            if grid[i+1][j][k] == 1:
                                grid[i+1][j][k] = 4
                            else:
                                grid[i+1][j][k] = 5
    #Mark entrance and exit
    grid[xMax-1][yMax-1][zMax-1] = 9
    grid[0][0][0] = 2
    
    #This is not an ideal way of padding the array with 0's
    newGrid = np.zeros(shape=(xMax+2,yMax+2,yMax+2), dtype = np.int8)
    for i in range(len(newGrid)):
        for j in range(len(newGrid[0])):
            for k in range(len(newGrid[0][0])):
                if i != 0 and j != 0 and k != 0 and i != (len(newGrid) - 1) and j != (len(newGrid[0]) - 1) and k != (len(newGrid[0][0]) - 1):
                    newGrid[i][j][k] = grid[i-1][j-1][k-1]
    
    return newGrid






