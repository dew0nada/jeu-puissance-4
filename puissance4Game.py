import tkinter as tk

ROWS, COLS = 6, 7

grid = [[0] * COLS for _ in range(ROWS)]
win = False
player = 1

def verify_last_ligne(col):
    return 0 <= col < COLS and grid[0][col] == 0

def check_win():
    
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

def addBlock(event):
    global win, player
    i = (event.y - 10) // 60
    j = (event.x - 10) // 60

    if i != 0 or not(0 <= j < COLS):
        return
    elif win == True or not verify_last_ligne(j):
        #this is a check to avoid playing after game is done
        return

    #check for correct line (gravity rule)
    for t in range(ROWS):
        if grid[5-t][j]== 0:
            grid[5-t][j] = player
            buildV()
            break
    
    if check_win():
        win = True
        curPlayer.config(text= "player" + str(player) + " won!!")
    elif not verify_last_ligne(j):
        curPlayer.config(text= "DRAW!")
    else: #if game didnt end change player (+ gui)
        player = 3 - player
        curPlayer.config(text= "player" + str(player) + " plays")


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

canvas = tk.Canvas(root,
                   width=430, height=370,
                   bg="#3F6D9E",
                   highlightthickness=5, highlightbackground="#38618C")
canvas.pack(side= "left")
canvas.bind("<Button-1>", addBlock)

buildV()
root.mainloop()