import tkinter as tk
import timer

from tkinter import ttk
from tkinter import font

from logic import *


class App:
    def __init__(self):
        self.win = tk.Tk()
        self.win.geometry('685x820')
        self.win.resizable(False, False)
        self.win.title('TETRIS')
        self.win.bind('<Escape>', self.destroy_all)

        self.level_label = None
        self.line_label = None
        self.time_label = None
        self.score_label = None
        self.board = None
        self.keep_board = None
        self.next_board = []

        self.level = 1
        self.goal_hit = 10
        self.curr_hit = 0
        self.score = 0

        self.timer = timer.Timer()
        self.queue = [Block() for _ in range(4)]

        self.build_widgets()

    def build_widgets(self):
        default_font = font.Font(family='Malgun Gothic', size=20)
        style = ttk.Style(self.win)
        style.configure('TLabel', font=default_font)
        style.map('TLabel', background=[(None, 'white')])

        keep_label = ttk.Label(text='KEEP', anchor='center')
        keep_label.place(x=10, y=12, width=120, height=40)

        self.keep_board = tk.Canvas(self.win, width=120, height=120, bg='white', relief='solid', bd=1)
        for i in range(1, 4):
            self.keep_board.create_line(0, 30*i, 120, 30*i, fill='light gray')
            self.keep_board.create_line(30*i, 0, 30*i, 120, fill='light gray')
        self.keep_board.place(x=8, y=60)

        level_title = ttk.Label(text='LEVEL', anchor='center')
        level_title.place(x=10, y=500, width=120, height=40)
        self.level_label = ttk.Label(text=self.level, anchor='e')
        self.level_label.place(x=10, y=550, width=120, height=40)

        line_title = ttk.Label(text='LINES', anchor='center')
        line_title.place(x=10, y=600, width=120, height=40)
        self.line_label = ttk.Label(text=str(self.curr_hit) + '/' + str(self.goal_hit), anchor='e')
        self.line_label.place(x=10, y=650, width=120, height=40)

        self.board = tk.Canvas(self.win, width=400, height=800, bg='white', relief='solid', bd=2)
        self.board.place(x=140, y=10)

        for y in range(1, 20):
            self.board.create_line(0, 40 * y, 500, 40 * y, fill='light gray')
        for x in range(1, 10):
            self.board.create_line(40 * x, 0, 40 * x, 800, fill='light gray')

        next_label = ttk.Label(text='NEXT', anchor='center')
        next_label.place(x=552, y=12, width=120, height=40)
        for i in range(3):
            self.next_board.append(tk.Canvas(self.win, width=120, height=120, bg='white', relief='solid', bd=1))
            self.next_board[i].place(x=550, y=60+i*130)
        for board in self.next_board:
            for i in range(1, 4):
                board.create_line(0, 30*i, 120, 30*i, fill='light gray')
                board.create_line(30*i, 0, 30*i, 120, fill='light gray')

        time_title = ttk.Label(text='TIME', anchor='center')
        time_title.place(x=552, y=500, width=120, height=40)
        self.time_label = ttk.Label(text='00:00', anchor='center')
        self.time_label.place(x=552, y=550, width=120, height=40)

        score_title = ttk.Label(text='SCORE', anchor='center')
        score_title.place(x=552, y=600, width=120, height=40)
        self.score_label = ttk.Label(text=self.score, anchor='e')
        self.score_label.place(x=552, y=650, width=120, height=40)

    def destroy_all(self, event=None):
        self.queue.clear()
        self.win.destroy()

    def update(self):
        self.timer.tick()
        text = self.timer.formatted_time()
        self.time_label.configure(text=text)
        self.win.after(1, self.update)

    def run(self):
        self.update()
        self.win.mainloop()

