import tkinter as tk
import math
import random

ROWS, COLS = 6, 7
DEPTH = 6
grid = [[0] * COLS for _ in range(ROWS)]
win = False
player = 1

def check_full_board():
    for i in range(COLS):
        if grid[0][i] == 0:
            return False
    return True

def check_win(player):
    
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(grid[r][c + i] == player for i in range(4)):
                return True

    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(grid[r + i][c] == player for i in range(4)):
                return True

    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(grid[r + i][c + i] == player for i in range(4)):
                return True

    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(grid[r - i][c + i] == player for i in range(4)):
                return True

    return False

def checkPossibleCols(grid):
    possibilities = []
    for i in range(COLS):
        if grid[0][i] == 0:
            possibilities.append(i)
    possibilities.sort(key=lambda x: abs(x - 4))
    return possibilities

def addBlock(col, player):
    global grid
    for t in range(ROWS):
        if grid[5-t][col]== 0:
            grid[5-t][col] = player
            return 5-t

def scale(): #binome
    return int(random.randint(0, 10000000))

def removeBlock(col, row):
    global grid
    grid[row][col] = 0
    return

def min_max(depth, alpha, beta, maxORmin):
    score = 0
    if check_win(2):
        return 10000000 - DEPTH + depth
    elif check_win(1):
        return -10000000 + DEPTH - depth
    elif check_full_board():
        return 0
    elif depth == 0:
        return scale()

    if maxORmin == 1:
        best = -math.inf
    else:
        best = math.inf

    for possibility in checkPossibleCols(grid):
        line = addBlock(possibility, 2)
        score = min_max(depth - 1, alpha, beta, 3-maxORmin)
        removeBlock(possibility, line)
        if maxORmin == 1: #max
            if best < score:
                best = score
            if best > alpha:
                alpha = best
        else: #min
            if best > score:
                best = score
            if best < beta:
                beta = best
        if alpha >= beta:
            break
    return best


def findMove():
    final_score = -math.inf
    final_col = None
    alpha, beta = -math.inf, math.inf

    for possibility in checkPossibleCols(grid):
        line = addBlock(possibility, 2)
        score = min_max(DEPTH - 1, alpha, beta, 1)
        removeBlock(possibility, line)
        if final_score < score:
            final_score = score
            final_col = possibility
        if final_score > alpha:
            alpha = final_score

    addBlock(final_col, 2)
    betweenTurn(2)






#------------gui fct-------------------

def buildV():
    canvas.delete("all")
    for i in range(ROWS):
        for j in range(COLS):
            x0 = j * (50 + 10) + 10
            y0 = i* (50 + 10) + 10
            x1 = x0 + 50
            y1 = y0 + 50
            if grid[i][j] == 0 :
                color = "#38618C"
            elif grid[i][j] == 1 :
                color = "#F783B0"
            else:
                color = "#E6F2EF"
            canvas.create_oval(x0, y0, x1, y1, fill= color, outline= "#38618C")

def addBlockHuman(event):
    i = (event.y - 10) // 60
    j = (event.x - 10) // 60

    if i != 0 or not(0 <= j < COLS):
        return
    elif win == True or not(grid[0][j] == 0) or player == 2:
        return

    addBlock(j, 1)
    betweenTurn(1)
    

def betweenTurn(playerC):
    global player, win

    buildV()

    if check_win(player):
        win = True
        curPlayer.config(text= "player" + str(player) + " won!!")
    elif check_full_board():
        curPlayer.config(text= "DRAW!")
    else:
        player = 3 - playerC
        if player == 2:
            curPlayer.config(text= "computer turn")
            findMove()
        else:
            curPlayer.config(text= "ur turn")



def restart():
    global win, player
    for r in range(ROWS):
        for c in range(COLS):
            grid[r][c] = 0
    win = False
    player = 1
    curPlayer.config(text= "restart text")
    buildV()

#---------------- gui part
root = tk.Tk()
root.title("jeu Puissance 4 (human VS human)")
root.geometry("900x400")
root.configure(bg="#151640")

title = tk.Label(root,
                 text="jeu Puissance 4\n(human VS human)",
                 fg="#151640", bg="#3F6D9E",
                 font=("Papyrus", 20, "bold"))
title.place(x= 450, y= 20)

curPlayer = tk.Label(root,
                 text= "player" + str(player) + " plays",
                 fg="#151640", bg="#3F6D9E",
                 font=("Papyrus", 20, "bold"))
curPlayer.place(x= 450, y= 150)

status = tk.Label(root,
                 text= " ",
                 fg="#3F6D9E", bg="#151640",
                 font=("Papyrus", 40, "bold"))
status.place(x= 450, y= 250)

restartBtn = tk.Button(root,
                 text= "Rejouer",
                 fg="#151640", bg="#F783B0",
                 font=("Papyrus", 16, "bold"),
                 command= restart)
restartBtn.place(x= 450, y= 320)

canvas = tk.Canvas(root,
                   width=430, height=370,
                   bg="#3F6D9E",
                   highlightthickness=5, highlightbackground="#38618C")
canvas.pack(side= "left")
canvas.bind("<Button-1>", addBlockHuman)

buildV()
root.mainloop()