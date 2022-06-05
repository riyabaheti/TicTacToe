import numpy as np

# returns whether or not the current board results in a draw
def isDraw(grid):
    count = np.count_nonzero(grid == ' ')
    return count != 0


# returns the winner of the game given a board status
def determineWinner(grid):
    for i in range(3):
        row = i * 3
        col = i
        if grid[row] == grid[row + 1] and grid[row + 1] == grid[row + 2]:
            return grid[row]
        if grid[col] == grid[col + 3] and grid[col + 3] == grid[col + 6]:
            return grid[col]
    if grid[0] == grid[4] and grid[4] == grid[8]:
        return grid[0]
    if grid[2] == grid[4] and grid[4] == grid[6]:
        return grid[2]
    return ' '

# returns whether userX has finished their turn
def getUserMoveX(grid, end_point, cursor):
    x = cursor[0]
    y = cursor[1]
    
    col = int(3 * y / end_point)
    row = int(3 * x / end_point)
    
    if grid[row * 3 + col] == ' ':
        grid[row * 3 + col] = 'X'
        return True
    return False

# returns whether userO has finished their turn
def getUserMoveO(grid, end_point, cursor):
    x = cursor[0]
    y = cursor[1]
    
    col = int(3 * y / end_point)
    row = int(3 * x / end_point)
    
    if grid[row * 3 + col] == ' ':
        grid[row * 3 + col] = 'O'
        return True
    return False