import cv2
import random

def drawEmptyGrid(frame, end_point):
    cv2.line(frame, (0, int(end_point / 3)), (end_point, int(end_point / 3)), (0, 0, 0), 5)
    cv2.line(frame, (0, int(2 * end_point / 3)), (end_point, int(2 * end_point / 3)), (0, 0, 0), 5)
    cv2.line(frame, (int(end_point / 3), 0), (int(end_point / 3), end_point), (0, 0, 0), 5)
    cv2.line(frame, (int(2 * end_point / 3), 0), (int(2 * end_point / 3), end_point), (0, 0, 0), 5)

def fillBoard(frame, end_point, grid, size):
    for i in range(len(grid)):
        if grid[i] == 'X':
            row = int(i / 3) * int(end_point / 3) + int(end_point / 6)
            col = int(i % 3) * int(end_point / 3) +int(end_point / 6)
            cv2.line(frame, (row + size, col + size), (row - size, col - size), (0, 0, 0), 5)
            cv2.line(frame, (row - size, col + size), (row + size, col - size), (0, 0, 0), 5)
        elif grid[i] == 'O':
            row = int(i / 3) * int(end_point / 3) + int(end_point / 6)
            col = int(i % 3) * int(end_point / 3) + int(end_point / 6)
            cv2.circle(frame, (row, col), size, (0, 0, 0), 5)
            
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
            
def isDraw(grid):
    for g in grid:
        if g == ' ':
            return False
    return True

def makeComputerMove(grid):
    options = []
    for i in range(len(grid)):
        if grid[i] == ' ':
            options.append(i)
    grid[random.choice(options)] = 'X'

def getUserMove(grid, end_point, cursor):
    x = cursor[0]
    y = cursor[1]
    
    col = int(3 * y / end_point)
    row = int(3 * x / end_point)
    print(row, col)
    
    if grid[row * 3 + col] == ' ':
        grid[row * 3 + col] = 'O'
        return True
    return False


def getContours(mask, frame):
    center = (-1, -1)
    
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        center = (int(x), int(y))

        if radius > 5:
            cv2.circle(frame, center, int(radius), (0, 255, 255), 2)
    
    return frame, center


camera = cv2.VideoCapture(0)


grid = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
playerMove = True

gameOngoing = True

while gameOngoing:
    frame = camera.read()[1]

    frame = cv2.resize(frame, (600, 600))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, (30, 90, 5), (70, 255, 255))

    frame, cursor = getContours(mask, frame)

    drawEmptyGrid(frame, 600)
    fillBoard(frame, 600, grid, 50)

    key = cv2.waitKey(1) & 0xFF

    if playerMove:
        if key == ord("p") and (getUserMove(grid, 600, cursor)):
            playerMove = False
    else:
        makeComputerMove(grid)
        playerMove = True

    if determineWinner(grid) != ' ':
        print(determineWinner(grid) + ' Won the Game!')
        gameOngoing = False
    elif isDraw(grid):
        print('Game over! It was a draw :(')
        gameOngoing = False


    cv2.imshow("Frame", frame)    

camera.release()
cv2.destroyAllWindows()
