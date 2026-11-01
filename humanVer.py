import tkinter as tk

grid = [[0] * 7 for _ in range(6)]
win = False
player = 1


#fighting the urge to write code w nethna but 3ndi binome
def checkLign():
    return False

def checkWin():
    return False

def buildV():
    canvas.delete("all")
    for i in range(6):
        for j in range(7):
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

def clicked(event):
    global win, player
    i = (event.y - 10) // 60
    j = (event.x - 10) // 60

    if i != 0 or not(0 <= j < 7):
        return
    elif win == True or checkLign():
        return
    
    for t in range(6):
        if grid[5-t][j]== 0:
            grid[5-t][j] = player
            buildV()
            break
    
    if checkWin():
        win = True
        print("player" + player + " won!!")
    elif checkLign():
        curPlayer.config(text= "DRAW!")
    else:
        player = 3 - player


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
                 text= "current player :",
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
canvas.bind("<Button-1>", clicked)

buildV()
root.mainloop()