import pygame
import numpy as np
import random
import math


A_star = True #IF false - Dikstra's algorithm

GRID_SIZE = 25
WINDOW_SIZE = GRID_SIZE*GRID_SIZE
START_POSITION = (1,1)
END_POSITION = (24,19)
MARKED = 50



#Define the window
win = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Client")


#Cell class
class Cell:
    def __init__(self, row, col):
        self.row, self.col = row, col
        #g = real distance, h = heuristic
        self.g, self.h = 0, 0
        #f = the cost function
        self.f = self.g + self.h

        self.previous = None

        self.distance_from_start = 1000

    def Draw(self,win,color):
        x = self.row * (WINDOW_SIZE / GRID_SIZE) + 1
        y = self.col * (WINDOW_SIZE / GRID_SIZE) + 1
        pygame.draw.rect(win,color,(x,y,GRID_SIZE-1,GRID_SIZE-1))


    def GetNeighborsTuples(self):
        #Tuple with shape (x,y)
        tmp_lst = []
        row, col = self.row, self.col
        if row > 0:
            tmp_lst.append((col, row-1))
        if row < GRID_SIZE-1:
            tmp_lst.append((col, row+1))
        if col > 0:
            tmp_lst.append((col-1,row))
        if col < GRID_SIZE-1:
            tmp_lst.append((col+1,row))

        return tmp_lst




def redrawWindow(win,grid,open_set,closed_set,path,marked):
    win.fill((0,0,0))
    #Draw grid
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] in marked:
                continue
            elif grid[i][j] in path:
                grid[i][j].Draw(win, (0, 0, 255))
            elif grid[i][j] in open_set:
                grid[i][j].Draw(win,(0,255,0))
            elif grid[i][j] in closed_set:
                grid[i][j].Draw(win, (255, 0, 0))
            else:
                grid[i][j].Draw(win, (255, 255, 255))

    pygame.display.update()



def CheckWindowInterrupt():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
            pygame.quit()

    return False


def FindLowestFValue(open_set):
    min_cell = open_set[0]
    min = min_cell.f
    for cell in open_set:
        if cell.f < min:
            min_cell = cell
            min = min_cell.f

    return min_cell


def heuristic_score(neighbor, goal):
    oclidian_distance = abs(goal.row - neighbor.row) + abs(goal.col - neighbor.col)
    return oclidian_distance


def GenerateMarkedNodes(grid,num,goal,start_node):
    marked = [start_node]
    for i in range(num):
        row = random.randint(0, GRID_SIZE-1)
        col = random.randint(0, GRID_SIZE-1)
        while grid[row][col] in marked or marked == goal or marked == start_node:
            row = random.randint(0, GRID_SIZE-1)
            col = random.randint(0, GRID_SIZE-1)
        marked.append(grid[row][col])

    return marked


def CreateGrid(size):
    grid = []
    for i in range(size):
        tmp = []
        for j in range(size):
            tmp.append(Cell(i, j))
        grid.append(tmp)

    return grid



def GridSearch(grid, start, goal,marked = []):
    visited = [[False for i in range(len(grid[0]))] for j in range(len(grid))]
    visited[START_POSITION[1]][START_POSITION[0]] = True
    q = [start]
    path = []
    while len(q) > 0:
        current = q.pop()
        visited[current.row][current.col] = True
        if current == goal:
            while current.previous is not None:
                path.append((current.row,current.col))
                current = current.previous
            return path

        neighbors = [grid[tup[1]][tup[0]] for tup in current.GetNeighborsTuples()]
        for neighbor in neighbors:
            if not visited[neighbor.row][neighbor.col] and neighbor not in marked:
                q.append(neighbor)
                neighbor.previous = current



    return []


def FindClosestNode(open_set):
    min_node = open_set[0]
    for node in open_set:
        if node.distance_from_start < min_node.distance_from_start:
            min_node = node

    return min_node



def main():

    clock = pygame.time.Clock()
    #Initialize the grid = list of lists of cell objects
    grid = CreateGrid(GRID_SIZE)

    start_node = grid[START_POSITION[1]][START_POSITION[0]]
    start_node.distance_from_start = 0
    goal = grid[END_POSITION[1]][END_POSITION[0]]

    closed_set = []
    open_set = [start_node]


    marked = GenerateMarkedNodes(grid,MARKED,goal,start_node)
    finished = False
    path = []
    while len(open_set) > 0:

        clock.tick(100)
        if CheckWindowInterrupt():
            break

        if finished:
            redrawWindow(win, grid, open_set, closed_set, path, marked)
            continue
        if A_star:

            #Find the node in openset which have the lowest f(n) value
            current = FindLowestFValue(open_set)
            if current == goal:
                print('Path found !!!')
                finished = True
                path.append(current)
                continue

            open_set.remove(current)
            closed_set.append(current)

            neighbors_tuples = current.GetNeighborsTuples()
            #neighbors = [grid[tup[1]][tup[0]] for tup in neighbors_tuples]
            neighbors = []
            for tup in neighbors_tuples:
                print(tup)
                tmp = grid[tup[1]][tup[0]]
                neighbors.append(tmp)

            for neighbor in neighbors:
                if neighbor in closed_set or neighbor in marked:
                    continue
                tmp_gScore = current.g + 1
                #If the neighbor not in openset or it is but its gScore < then its G in the openset
                if (neighbor not in open_set) or tmp_gScore < neighbor.g:
                    neighbor.g = tmp_gScore
                    neighbor.f = neighbor.g + heuristic_score(neighbor,goal)
                    neighbor.previous = current
                    if neighbor not in open_set:
                        open_set.append(neighbor)


            path = []
            tmp = current
            path.append(tmp)
            while tmp.previous != None:
                path.append(tmp.previous)
                tmp = tmp.previous

        else:
            current = FindClosestNode(open_set)
            print(len(open_set))
            open_set.remove(current)
            print(len(open_set))
            #visited[current.row][current.col] = True
            closed_set.append(current)
            if current == goal:

                while current.previous is not None:
                    path.append(current.previous)
                    current = current.previous
                finished = True

            neighbors = [grid[tup[1]][tup[0]] for tup in current.GetNeighborsTuples()]
            for neighbor in neighbors:
                if (neighbor not in closed_set) and (neighbor not in marked):
                    if current.distance_from_start + 1 < neighbor.distance_from_start:
                        neighbor.distance_from_start = current.distance_from_start + 1
                        neighbor.previous = current
                        open_set.append(neighbor)

        redrawWindow(win, grid,open_set,closed_set,path,marked)

    print('Done.')



if __name__ == "__main__":
    main()

