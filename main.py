import database as db
import tkinter as tk


def show():
    label = tk.Label(canvas, text=db.getAll())
    label.grid()


def quit():
    root.quit()


def mainScreen():
    tk.Label(canvas, text="Zakázky").grid()
    rows = db.get("10")

    canvasZ = tk.Canvas(canvas)
    canvasZ.grid()
    for row in rows:
        tk.Label(canvasZ, text=row).grid()


root = tk.Tk()
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
# root.attributes("-fullscreen", True)

canvas = tk.Canvas(root)
canvas.grid()

mainScreen()

# b = tk.Button(root, text="X", command=quit, bg="red", fg="white")
# b.grid(row=0, column=10)

addN = tk.Button(canvas, command=show, text="click")
addN.grid(row=1, column=0)

root.mainloop()
