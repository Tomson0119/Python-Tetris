import tkinter as tk

from tkinter import ttk


class App:
    def __init__(self):
        self.win = tk.Tk()
        self.win.geometry('600x800')
        self.win.resizable(False, False)
        self.win.title('TETRIS')
        self.win.bind('<Escape>', self.destroy_all)
        self.win.configure(bg='white')

        canvas = tk.Canvas(self.win, width=400, height=750)
        canvas.create_rectangle(0, 0, 100, 100, fill='red')
        canvas.move(10)
        canvas.pack()

    def destroy_all(self, event=None):
        self.win.destroy()

    def run(self):
        self.win.mainloop()

