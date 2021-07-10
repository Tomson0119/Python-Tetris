import tkinter as tk
import timer

from tkinter import ttk
from tkinter import font


class App:
    def __init__(self):
        self.win = tk.Tk()
        self.win.geometry('600x820')
        self.win.resizable(False, False)
        self.win.title('TETRIS')
        self.win.bind('<Escape>', self.destroy_all)

        self.timer = timer.Timer()

        default_font = font.Font(family='Malgun Gothic', size=20)
        style = ttk.Style(self.win)
        style.configure('TLabel', font=default_font)
        style.map('TLabel', background=[(None, 'white')])

        self.time_label = ttk.Label(text='00:00', anchor='center')
        self.time_label.place(x=420, y=600, width=160, height=50)

        self.board = tk.Canvas(self.win, width=400, height=800, bg='white')
        self.board.place(x=10, y=10)

        for y in range(1, 20):
            self.board.create_line(0, 40*y, 500, 40*y, fill='light gray')
        for x in range(1, 10):
            self.board.create_line(40*x, 0, 40*x, 800, fill='light gray')

        self.keep_board = tk.Canvas(self.win, width=160, height=160, bg='white')
        self.keep_board.place(x=420, y=10)

        for i in range(1, 4):
            self.keep_board.create_line(40*i, 0, 40*i, 160, fill='light gray')
            self.keep_board.create_line(0, 40*i, 160, 40*i, fill='light gray')

    def destroy_all(self, event=None):
        self.win.destroy()

    def update(self):
        self.timer.tick()
        text = self.timer.formatted_time()
        self.time_label.configure(text=text)
        self.win.after(1, self.update)

    def run(self):
        self.update()
        self.win.mainloop()

