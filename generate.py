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

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Define directions
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
DIRECTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]

# This sets the maze dimensions
# Number of rows and columns has to be odd
COLUMNS = 51
ROWS = 51

# The total width of the window should not exceed 720 px
WIDTH = round(720/COLUMNS)-1
HEIGHT = round(720/COLUMNS)-1

# This sets the margin between each cell
MARGIN = 1

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [(WIDTH+MARGIN)*COLUMNS, (HEIGHT+MARGIN)*ROWS]

# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
# 0 represents a filled cell (wall), 1 represents an emty cell (open)
#  x -->
# y
# |
# v
grid = []
for column in range(COLUMNS):
    # Add an empty array that will hold each cell
    # in this column
    grid.append([])
    for row in range(ROWS):
        grid[column].append(0)  # Append a cell, default value is 0 (wall)

# Initialize pygame
pygame.init()
 
# Initialize screen
screen = pygame.display.set_mode(WINDOW_SIZE)
 
# Set title of screen
pygame.display.set_caption("Array Backed Grid")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Define starting position and push it in stack
random.seed()
startPos = [random.randint(3, (COLUMNS-1)/2)*2-3, random.randint(3, (ROWS-1)/2)*2-3]
stack = [startPos]
grid[startPos[0]][startPos[1]] = 3
currentPos = startPos
endPos = startPos

stackMaxSize = 1

def findDir(pos):
    print("find direction")
    result = -1
    directions = [UP, DOWN, LEFT, RIGHT]
    while len(directions) != 0 and result == -1:
        rnd = random.randint(0, len(directions) - 1)
        dir = directions[rnd]
        if dir == UP:
            if pos[1] == 1:
                directions.remove(UP)
            elif grid[pos[0]][pos[1]-2] != 0:
                directions.remove(UP)
            else:
                result = dir
        elif dir == DOWN:
            if pos[1] == ROWS - 2:
                directions.remove(DOWN)
            elif grid[pos[0]][pos[1]+2] != 0:
                directions.remove(DOWN)
            else:
                result = dir
        elif dir == LEFT:
            if pos[0] == 1:
                directions.remove(LEFT)
            elif grid[pos[0]-2][pos[1]] != 0:
                directions.remove(LEFT)
            else:
                result = dir
        elif dir == RIGHT:
            if pos[0] == COLUMNS - 2:
                directions.remove(RIGHT)
            elif grid[pos[0]+2][pos[1]] != 0:
                directions.remove(RIGHT)
            else:
                result = dir
    return result

# -------- Drawing Maze Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
            continue
        elif event.type == pygame.KEYDOWN :  # If user press SPACE
            if event.key == pygame.K_SPACE:
                done = True  # Flag that we are done so we exit this loop
                continue
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            # Set that location to one
            grid[column][row] = 1
            print("Click ", pos, "Grid coordinates: ", column, row)

    # Set the screen background
    screen.fill(BLACK)
    
    print("current pos " + str(currentPos[0]) + ":"  + str(currentPos[1]))

    # Pick a random direction
    dir = findDir(currentPos)
    if dir == -1: # no possible direction, this is a dead end
        if len(stack) > 1:
            print("Dead End, go back !")
            grid[currentPos[0]][currentPos[1]] = 1
            currentPos = stack.pop() # returns the last element and remove it from list
            grid[currentPos[0]][currentPos[1]] = 2
        else:
            print("Stack is empty, exit !")
            #done = True

    elif dir == UP:
        print("Move UP")
        grid[currentPos[0]][currentPos[1]] = 1
        grid[currentPos[0]][currentPos[1]-1] = 1
        grid[currentPos[0]][currentPos[1]-2] = 2
        currentPos = [currentPos[0], currentPos[1]-2]
        stack.append(currentPos)

    elif dir == DOWN:
        print("Move DOWN")
        grid[currentPos[0]][currentPos[1]] = 1
        grid[currentPos[0]][currentPos[1]+1] = 1
        grid[currentPos[0]][currentPos[1]+2] = 2
        currentPos = [currentPos[0], currentPos[1]+2]
        stack.append(currentPos)

    elif dir == LEFT:
        print("Move LEFT")
        grid[currentPos[0]][currentPos[1]] = 1
        grid[currentPos[0]-1][currentPos[1]] = 1
        grid[currentPos[0]-2][currentPos[1]] = 2
        currentPos = [currentPos[0]-2, currentPos[1]]
        stack.append(currentPos)

    elif dir == RIGHT:
        print("Move RIGHT")
        grid[currentPos[0]][currentPos[1]] = 1
        grid[currentPos[0]+1][currentPos[1]] = 1
        grid[currentPos[0]+2][currentPos[1]] = 2
        currentPos = [currentPos[0]+2, currentPos[1]]
        stack.append(currentPos)

    # save the position of the most distant point from start
    if len(stack) > stackMaxSize:
        stackMaxSize = len(stack)
        grid[endPos[0]][endPos[1]] = 1
        endPos = currentPos

    grid[startPos[0]][startPos[1]] = 3
    grid[endPos[0]][endPos[1]] = 4

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
 
    # Limit to 60 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

grid[currentPos[0]][currentPos[1]] = 1
grid[startPos[0]][startPos[1]] = 3
grid[endPos[0]][endPos[1]] = 4

#initialize an array
arr = np.array(grid)
print(arr)
# open a binary file in write mode
file = open("maze", "wb")
# save array to the file
np.save(file, arr)
# close the file
file.close

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
