import cv2
from tkinter import *
from PIL import ImageTk,ImageChops

def drawEmptyBoard(frame, end_point):
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
            
def endOfGameBoard():
    root = Tk()
    root.title("Tic Tac Toe")

    def startGameAgain():
        frame.destroy()
        yesB.destroy()
        noB.destroy()
        root.destroy()
        runGame()

    def endGameCompletely():
        frame.destroy()
        frame.destroy()
        yesB.destroy()
        noB.destroy()
        root.destroy()

    frame = LabelFrame(root, text="Tic Tac Toe", padx=50, pady=50, bg="#66CCFF")
    frame.pack(padx=50, pady=50)

    instructions = Label(frame, text="Would you like to play again?", bg="#66CCFF")
    instructions.pack()

    yesB = Button(frame, text="Yes", background="white", command=startGameAgain)
    yesB.pack(pady=30)

    noB = Button(frame, text="No", background="white", command=endGameCompletely)
    noB.pack(pady=30)

    root.mainloop()


def startGameBoard():
    root = Tk()
    root.title("Tic Tac Toe")

    def destroyStartGrid():
        frame.destroy()
        b.destroy()
        root.destroy()

    frame = LabelFrame(root, text="Welcome to Webcam-Based Two Player Tic Tac Toe", padx=50, pady=50, bg="#66CCFF")
    frame.pack(padx=50, pady=50)

    startText = "Welcome to Tic Tac Toe. \n This is a webcam based two player tic tac toe game. \n"
    toPlay = "To play, press the start button below to begin the game, and the tic tac toe grid will pop up. \n"
    gameInstructions = "Make sure that one player has the red X pulled up on a handheld device, and the other player has the blue O. \n The X and O can be found in the resources folder or can be drawn as your convenience. The red X player starts. When it is each \n players\' the player will hold up their device in the grid space where they would like to place their move. When the red X \n player is ready to make their move (they are holding the red X in the correct frame), they will press the r key on the keyboard \n to make their move. Similarly, when the blue X player is ready to make their move, they will press the b key on the keyboard. \n When the game is over, the winner (or a message saying that the game is a draw), will print out in the terminal. At this point, \n you can choose to play again or quit. \n  Now press Start Game to begin!"

    instructions = Label(frame, text=startText + toPlay + gameInstructions, bg="#66CCFF")
    instructions.pack()

    b = Button(frame, text="Start Game", background="white", command=destroyStartGrid)
    b.pack(pady=50)

    root.mainloop()

from tictactoe import runGame