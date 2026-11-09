import tkinter as tk
import math

ROWS, COLS = 6, 7
DEPTH = 6
EMPTY, HUM, CPU = 0, 1, 2

W3, W2 = 5, 2          
W_CENTER = 3
THREAT_GOOD = 50       
THREAT_BAD = 10 

WINDOWS = []
for _r in range(ROWS):
    for _c in range(COLS):
        for _dr, _dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
            _er, _ec = _r + 3 * _dr, _c + 3 * _dc
            if 0 <= _er < ROWS and 0 <= _ec < COLS:
                WINDOWS.append(tuple((_r + i * _dr, _c + i * _dc) for i in range(4)))

grid = [[EMPTY] * COLS for _ in range(ROWS)]
win = False
player = HUM

def check_full_board():
    for i in range(COLS):
        if grid[0][i] == EMPTY:
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
        if grid[0][i] == EMPTY:
            possibilities.append(i)
    possibilities.sort(key=lambda x: abs(x - 3))
    return possibilities

def addBlock(col, player):
    global grid
    for t in range(ROWS):
        if grid[5-t][col]== EMPTY:
            grid[5-t][col] = player
            return 5-t

def scale(): #binome
    s = eval_B()
    threats_cpu, threats_hum = set(), set()
    for w in WINDOWS:
        cpu = hum = 0
        empty = None
        for r, c in w:
            v = grid[r][c]
            if v == CPU:
                cpu += 1
            elif v == HUM:
                hum += 1
            else:
                empty = (r, c)
        if cpu == 3 and hum == 0:
            threats_cpu.add(empty)
        elif hum == 3 and cpu == 0:
            threats_hum.add(empty)
    for r, c in threats_cpu:
        if r > 0 and grid[r - 1][c] == EMPTY:
            s += THREAT_GOOD if (r + 1) % 2 == 0 else THREAT_BAD
    for r, c in threats_hum:
        if r > 0 and grid[r - 1][c] == EMPTY:
            s -= THREAT_GOOD if (r + 1) % 2 == 1 else THREAT_BAD
    return s

def eval_B():
    s = 0
    for w in WINDOWS:
        cpu = hum = 0
        for r, c in w:
            v = grid[r][c]
            if v == CPU:
                cpu += 1
            elif v == HUM:
                hum += 1
        if hum == 0:                
            if cpu == 3:
                s += W3
            elif cpu == 2:
                s += W2
        elif cpu == 0:               
            if hum == 3:
                s -= W3
            elif hum == 2:
                s -= W2
    for r in range(ROWS):             
        if grid[r][3] == CPU:
            s += W_CENTER
        elif grid[r][3] == HUM:
            s -= W_CENTER
    return s

def removeBlock(col, row):
    global grid
    grid[row][col] = EMPTY
    return

def min_max(depth, alpha, beta, maxORmin):

    if check_win(CPU):
        return 10000000 - DEPTH + depth
    elif check_win(HUM):
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
        line = addBlock(possibility, CPU)
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



#------------ gameplay fct

def findMove():
    final_score = -math.inf
    final_col = None
    alpha, beta = -math.inf, math.inf

    for possibility in checkPossibleCols(grid):
        line = addBlock(possibility, CPU)
        score = min_max(DEPTH - 1, alpha, beta, 1)
        removeBlock(possibility, line)
        if final_score < score:
            final_score = score
            final_col = possibility
        if final_score > alpha:
            alpha = final_score

    addBlock(final_col, CPU)
    betweenTurn(CPU)

def addBlockHuman(event):
    computerStart.place_forget()
    i = (event.y - 10) // 60
    j = (event.x - 10) // 60

    if i != 0 or not(0 <= j < COLS):
        return
    elif win == True or not(grid[0][j] == 0) or player == CPU:
        return

    addBlock(j, HUM)
    betweenTurn(HUM)
    
def betweenTurn(playerC):
    global player, win

    buildV()

    if check_win(player):
        win = True
        if player == HUM:
            curPlayer.config(text= "you won!!")
        else:
            curPlayer.config(text= "computer won!!")
    elif check_full_board():
        curPlayer.config(text= "DRAW!")
    else:
        player = 3 - playerC
        if player == CPU:
            curPlayer.config(text= "computer turn")
            root.after(200,findMove)
        else:
            curPlayer.config(text= "your turn")

def restart():
    global win, player
    for r in range(ROWS):
        for c in range(COLS):
            grid[r][c] = EMPTY
    win = False
    player = HUM
    curPlayer.config(text= "you start")
    buildV()
    computerStart.place(x=450, y=250)

def letComputerStart():
    global player
    player = CPU
    curPlayer.config(text= "computer start")
    root.after(200,findMove)
    computerStart.place_forget()



#---------------- GUI

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

root = tk.Tk()
root.title("jeu Puissance 4 (human VS computer)")
root.geometry("900x400")
root.configure(bg="#151640")

title = tk.Label(root,
                 text="jeu Puissance 4\n(human VS computer)",
                 fg="#151640", bg="#3F6D9E",
                 font=("Papyrus", 20, "bold"))
title.place(x= 450, y= 20)

curPlayer = tk.Label(root,
                 text= "you start",
                 fg="#151640", bg="#3F6D9E",
                 font=("Papyrus", 20, "bold"))
curPlayer.place(x= 450, y= 150)

computerStart = tk.Button(root,
                 text= "Let computer start",
                 fg="#151640", bg="#E6F2EF",
                 font=("Papyrus", 16, "bold"),
                 command= letComputerStart)
computerStart.place(x= 450, y= 250)


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
