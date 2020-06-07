"""
 Example program to show using an array to back a grid on-screen.
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
 Explanation video: http://youtu.be/mdTeqiWyFnc
"""
import pygame
import random
import numpy as np
import sys

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# This sets the margin between each cell
MARGIN = 1

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 7
HEIGHT = 7

class Cell(object):
    def __init__(self, x, y):
        """
        Initialize new cell
 
        @param x cell x coordinate
        @param y cell y coordinate
        """
        self.x = x
        self.y = y
        self.cost = 0 # total cost
        self.distance = 0 # distance
        self.heuristic = 0 # heuristic
        self.parent = None

def get_heuristic_manhattan(cell):
    """
    Compute the heuristic value H for a cell: manhattan distance between
    this cell and the ending cell multiply by 10.
    @param cell
    @returns heuristic value H
    """
    return 10 * (abs(cell.x - endPos.x) + abs(cell.y - endPos.y))

def get_heuristic_euclidian(cell):
    """
    Compute the heuristic value H for a cell: square euclidian distance
    between this cell and the ending cell.
    @param cell
    @returns heuristic value H
    """
    return pow(cell.x - endPos.x, 2) + pow(cell.y - endPos.y, 2)

def get_distance(c1, c2):
    return abs(c2.x - c1.x) + abs(c2.x - c1.x)

def compare_cells(c1, c2):
       if c1.heuristic < c2.heuristic:
           return 1
       elif c1.heuristic  == c2.heuristic:
           return 0
       else:
           return -1

def get_neighbours(cell, grid):
    """
    Returns a list of walkable neighbours of the cell provided as argument
    @param cell
    @returns cells list
    """
    cells = []
    if cell.x > 0 and grid[cell.x-1][cell.y] != 0:
        cells.append(Cell(cell.x-1, cell.y))
    if cell.y > 0 and grid[cell.x][cell.y-1] != 0:
        cells.append(Cell(cell.x, cell.y-1))
    if cell.x < COLUMNS - 1 and grid[cell.x+1][cell.y] != 0:
        cells.append(Cell(cell.x+1, cell.y))
    if cell.y < ROWS - 1 and grid[cell.x][cell.y+1] != 0:
        cells.append(Cell(cell.x, cell.y+1))

    print("-> [%d, %d] neighbours are: " % (cell.x, cell.y), end = '')
    for v in cells:
        print(" [%d, %d]" % (v.x, v.y), end = '')
    print("")
    return cells

def insert_sorted_cost(list, cell):
    """
    Insert a cell in a list and returns this new list sorted in a 
    descendant order (highest cost first, lowest cost last)
    @param cell
    @param cells list
    @returns ordered cells list
    """
    display_list(list, "insert [%d, %d] (%d) in initial list : " % (cell.x, cell.y, cell.cost))

    if len(list) > 0:
        print("initial list is not empty")
        for i in range (0, len(list), 1):
            print("compare cell with position %d: [%d, %d] (%d)"%(i, list[i].x, list[i].y, list[i].cost))
            if cell.cost > list[i].cost:
                print("cell cost is higher, insert it at position %d"%(i))
                list.insert(i, cell)
                display_list(list, "resulting list : ")
                return list
    else:
        print("original list is empty")
    print("append cell to the end")
    list.append(cell)
    display_list(list, "resulting list : ")
    return list

def build_path(position, start, list):

    path = []
    path.insert(0, position)
    while len(list) > 0 and position.x != start.x and position.y != start.y:
        position = list.pop()
        path.insert(0, position)

    return path

def draw_grid(grid):
    # Draw the grid
    for column in range(COLUMNS):
        for row in range(ROWS):
            color = WHITE
            if grid[column][row] == 1:
                color = BLACK
            elif grid[column][row] == 2:
                color = RED
            elif grid[column][row] == 3:
                color = GREEN
            elif grid[column][row] == 4:
                color = BLUE
            pygame.draw.rect(screen,
                            color,
                            [(MARGIN + WIDTH) * column + MARGIN,
                            (MARGIN + HEIGHT) * row + MARGIN,
                            WIDTH,
                            HEIGHT])

def wait():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN :  # If user press a key
                return

def display_list(list, title = ""):
    print(title, end = '')
    for v in list:
        print(" [%d, %d] (%d/%d)" % (v.x, v.y, v.cost, v.distance), end = '')
    print("")

def is_in_list(cell, list):
    for v in list:
        if v.x == cell.x and v.y == cell.y:
            return True
    return False

def searchPath(startPos, endPos, grid):
    # yet_to_visit_list is a descendant ordered list of cells (highest cost first, lowest cost last)
    yet_to_visit_list = [startPos]
    visited_list = []

    # Loop until the user clicks the close button.
    done = False
    iterations = 0

    # -------- A star Loop -----------
    while len(yet_to_visit_list) > 0 and not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
                continue
            if event.type == pygame.KEYDOWN :  # If user press a key
                if event.key == pygame.K_ESCAPE:
                    done = True  # Flag that we are done so we exit this loop
                    continue
                elif event.key == pygame.K_SPACE:
                    wait()
    
        # Set the screen background
        screen.fill(BLACK)
        draw_grid(grid)    

        # get lower cost cell yet to visit
        currentCell = yet_to_visit_list.pop()
        print("----------------------------------------------------------")
        print("## Next cell (%d, %d)" % (currentCell.x, currentCell.y))
        # move lowest cost cell from open list to closed list
        visited_list.append(currentCell)
        grid[currentCell.x][currentCell.y] = 2
        iterations += 1

        # stop the loop if reached the end position
        if currentCell.x == endPos.x and currentCell.y == endPos.y:
            break

        cells = get_neighbours(currentCell, grid)
        for v in cells:
            if is_in_list(v, visited_list) or is_in_list(v, yet_to_visit_list):
            #if is_in_list(v, visited_list):
                print(" --> [%d, %d] has already been visited" % (v.x, v.y))
                continue

            v.parent = currentCell
            v.distance = currentCell.distance + 1
            v.heuristic = get_heuristic_euclidian(v)
            v.cost = v.heuristic + v.distance
            insert_sorted_cost(yet_to_visit_list, v)
            #visited_list.append(v)

        display_list(yet_to_visit_list, "open list: ")
        #display_list(visited_list, "closed list: ")
        # Limit to 60 frames per second
        clock.tick(60)
    
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    path = build_path(currentCell, startPos, visited_list)

    return path, iterations

if __name__ == '__main__':
    # open the file in read binary mode
    file = open("maze", "rb")
    #read the file to numpy array
    grid = np.load(file)
    print(grid)
    # close the file
    file.close

    # This sets the maze dimensions
    # Number of rows and columns has to be odd
    COLUMNS = len(grid)
    ROWS = len(grid[0])

    # Set the HEIGHT and WIDTH of the screen
    WINDOW_SIZE = [(WIDTH+MARGIN)*COLUMNS, (HEIGHT+MARGIN)*ROWS]

    # Initialize pygame
    pygame.init()
    
    # Initialize screen
    screen = pygame.display.set_mode(WINDOW_SIZE)
    
    # Set title of screen
    pygame.display.set_caption("Array Backed Grid")

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # Find ending and starting point
    for column in range(COLUMNS):
        # Add an empty array that will hold each cell
        # in this column
        for row in range(ROWS):
            if grid[column][row] == 3:
                startPos = Cell(column, row)
            elif grid[column][row] == 4:
                endPos = Cell(column, row)

    print("Starting from " + str(startPos.x) + ":" + str(startPos.y))
    print("Going to " + str(endPos.x) + ":" + str(endPos.y))

    path, iterations = searchPath(startPos, endPos, grid)
    display_list(path, "resulting path")
    print("in %d itertations" % (iterations))
    # Loop until the user clicks the close button.
    done = False

    # -------- Wait user event -----------
    wait()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()

