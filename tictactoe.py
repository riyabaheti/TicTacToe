import random
from tkinter import *
from PIL import ImageTk,ImageChops

from board import *
from gamestatus import *

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

def playerTurn(grid, playerMove, frame, hsv):
    # true = userX
    if playerMove:
        mask = cv2.inRange(hsv, (0, 100, 100), (10, 255, 255))

        frame, cursor = getContours(mask, frame)

        drawEmptyBoard(frame, 600)
        fillBoard(frame, 600, grid, 50)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("r") and (getUserMoveX(grid, 600, cursor)):
            playerMove = False
    else: # true = userO
        mask = cv2.inRange(hsv, (110, 50, 50), (130, 255, 255))

        frame, cursor = getContours(mask, frame)

        drawEmptyBoard(frame, 600)
        fillBoard(frame, 600, grid, 50)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("b") and (getUserMoveO(grid, 600, cursor)):
            playerMove = True



def runGame():
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    grid = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

    # true = userX
    # false = userO
    player_move = True

    is_active_game = True

    while is_active_game:
        frame = camera.read()[1]

        frame = cv2.resize(frame, (600, 600))
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        playerTurn(grid, player_move, frame, hsv)

        currentWinner = determineWinner(grid)
        if currentWinner != ' ':
            if currentWinner == 'X':
                print('Red (X) won the Game!')
            else:
                print('Blue (O) won the Game!')
            endOfGameBoard()
            is_active_game = False
        elif isDraw(grid):
            print('Game over! It was a draw :(')
            endOfGameBoard()
            is_active_game = False


        cv2.imshow("Frame", frame)    

    camera.release()
    cv2.destroyAllWindows()

