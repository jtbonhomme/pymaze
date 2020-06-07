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

# This sets the WIDTH and HEIGHT of each grid location
# The total width of the window should not exceed 720 px
WIDTH = round(720/COLUMNS)-1
HEIGHT = round(720/COLUMNS)-1

# This sets the margin between each cell
MARGIN = 1

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [(WIDTH+MARGIN)*COLUMNS, (HEIGHT+MARGIN)*ROWS]

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

# -------- Drawing Maze Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
            continue
        if event.type == pygame.KEYDOWN :  # If user press SPACE
            if event.key == pygame.K_SPACE:
                done = True  # Flag that we are done so we exit this loop
                continue
 
    # Set the screen background
    screen.fill(BLACK)

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

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
