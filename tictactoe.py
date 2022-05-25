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
            cv2.line(frame, (row + size, col + size), (row - size, col - size), (0, 0, 255), 5)
            cv2.line(frame, (row - size, col + size), (row + size, col - size), (0, 0, 255), 5)
        if grid[i] == 'O':
            row = int(i / 3) * int(end_point / 3) + int(end_point / 6)
            col = int(i % 3) * int(end_point / 3) + int(end_point / 6)
            cv2.circle(frame, (row, col), size, (255, 0, 0), 5)
            
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

def getRedUserMove(grid, end_point, cursor):
    x = cursor[0]
    y = cursor[1]
    
    col = int(3 * y / end_point)
    row = int(3 * x / end_point)
    
    if grid[row * 3 + col] == ' ':
        grid[row * 3 + col] = 'X'
        return True
    return False

def getBlueUserMove(grid, end_point, cursor):
    x = cursor[0]
    y = cursor[1]
    
    col = int(3 * y / end_point)
    row = int(3 * x / end_point)
    
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


def runGame():
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)


    grid = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    playerMove = True

    gameOngoing = True

    while gameOngoing:
        frame = camera.read()[1]

        frame = cv2.resize(frame, (600, 600))
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        if playerMove:
            mask = cv2.inRange(hsv, (0, 100, 100), (10, 255, 255))

            frame, cursor = getContours(mask, frame)

            drawEmptyGrid(frame, 600)
            fillBoard(frame, 600, grid, 50)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("r") and (getRedUserMove(grid, 600, cursor)):
                playerMove = False
        else:
            mask = cv2.inRange(hsv, (110, 50, 50), (130, 255, 255))

            frame, cursor = getContours(mask, frame)

            drawEmptyGrid(frame, 600)
            fillBoard(frame, 600, grid, 50)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("b") and (getBlueUserMove(grid, 600, cursor)):
                playerMove = True

        if determineWinner(grid) != ' ':
            if determineWinner(grid) == 'X':
                print('Red (X) won the Game!')
            else:
                print('Blue (O) won the Game!')
            gameOngoing = False
        elif isDraw(grid):
            print('Game over! It was a draw :(')
            gameOngoing = False


        cv2.imshow("Frame", frame)    

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    print("Welcome to Tic Tac Toe.")
    print("Press i to see instructions.")
    print("Press q to quit.")
    print("Press s to start!")
    playing = True

    while playing:
        val = input("Enter your letter:")
        if val == 'i':
            print('This is a webcam based two player tic tac toe game.')
            print('To play, press s when prompted to start the game, and the tic tac toe grid will pop up.')
            print('Make sure that one player has the red X pulled up on a handheld device, and the other player has the blue O.')
            print('The X and O can be found in the resources folder.')
            print('The red X player starts. When it is each players\' the player will hold up their device in the grid space where they would like to place their move.')
            print('When the red X player is ready to make their move (they are holding the red X in the correct frame), they will press the r key on the keyboard to make their move.')
            print('Similarly, when the blue X player is ready to make their move, they will press the b key on the keyboard.')
            print('When the game is over, the winner (or a message saying that the game is a draw), will print out in the terminal.')
            print('At this point, you can choose to play again, see the instructions again, or quit.')
            print("Now press s to start!")
        elif val == 's':
            runGame()
            print("Thanks for playing!")
        elif val == 'q':
            playing = False
            print("Goodbye!")
        else:
            print("Sorry, enter a valid letter.")

