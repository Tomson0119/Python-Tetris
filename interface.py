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
        self.win.bind('<Key>', self.get_input)

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
        self.queue = [Block() for _ in range(3)]

        self.build_widgets()
        self.initialize_board()

    def build_widgets(self):
        default_font = font.Font(family='Malgun Gothic', size=20)
        style = ttk.Style(self.win)
        style.configure('TLabel', font=default_font)
        style.map('TLabel', background=[(None, 'white')])

        keep_label = ttk.Label(text='KEEP', anchor='center')
        keep_label.place(x=10, y=12, width=120, height=40)

        self.keep_board = MyCanvas(self.win, (117, 117), (30, 30))
        self.keep_board.draw_grid(4, 4)
        self.keep_board.place(8, 60)

        level_title = ttk.Label(text='LEVEL', anchor='center')
        level_title.place(x=10, y=500, width=120, height=40)
        self.level_label = ttk.Label(text=self.level, anchor='e')
        self.level_label.place(x=10, y=550, width=120, height=40)

        line_title = ttk.Label(text='LINES', anchor='center')
        line_title.place(x=10, y=600, width=120, height=40)
        self.line_label = ttk.Label(text=str(self.curr_hit) + '/' + str(self.goal_hit), anchor='e')
        self.line_label.place(x=10, y=650, width=120, height=40)

        self.board = MyCanvas(self.win, (400, 800), (40, 40), border=2)
        self.board.draw_grid(20, 10)
        self.board.place(140, 10)

        next_label = ttk.Label(text='NEXT', anchor='center')
        next_label.place(x=552, y=12, width=120, height=40)
        for i in range(3):
            self.next_board.append(MyCanvas(self.win, (117, 117), (30, 30)))
            self.next_board[i].place(550, 60+i*130)
        for board in self.next_board:
            board.draw_grid(4, 4)

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

    def initialize_board(self):
        for i in range(3):
            self.fill_next_board(i)

    def fill_next_board(self, idx):
        color = self.queue[idx].color
        for p in self.queue[idx].get_pos():
            self.next_board[idx].draw_rectangle(p, color)

    def update(self):
        self.timer.tick()
        text = self.timer.formatted_time()
        self.time_label.configure(text=text)

        if len(self.queue) < 3:
            self.queue.append(Block())
            self.fill_next_board(2)

        self.win.after(1, self.update)

    def get_input(self, event=None):
        if event and event.keysym == 'Escape':
            self.destroy_all()
        elif event and event.keysym == 'space':
            self.queue.pop(0)

    def run(self):
        self.update()
        self.win.mainloop()


class MyCanvas:
    def __init__(self, master, size, block_size, border=1):
        self.tw, self.th = size
        self.bw, self.bh = block_size
        self.canvas = tk.Canvas(master, width=self.tw, height=self.th, bg='white', relief='solid', bd=border)

    def place(self, px, py):
        self.canvas.place(x=px, y=py)

    def draw_grid(self, rows, cols):
        for i in range(1, rows):
            self.canvas.create_line(2, self.bh*i, self.tw+2, self.bh*i, fill='light gray')
        for j in range(1, cols):
            self.canvas.create_line(self.bw*j, 2, self.bw*j, self.th+2, fill='light gray')

    def draw_rectangle(self, p, color):
        x, y = MyCanvas.calc_coord(30, p[0], p[1])
        nx, ny = MyCanvas.calc_coord(30, p[0] + 1, p[1] + 1)
        self.canvas.create_rectangle(x, y, nx, ny, fill=color)

    @staticmethod
    def calc_coord(size, r, c):
        return size * c, size * r