import tkinter as tk
from util import *


class MyCanvas:
    def __init__(self, master, size, block_size, row, col, bd=1):
        self.tw, self.th = size
        self.bw, self.bh = block_size
        self.rows, self.cols = row, col

        self.canvas = tk.Canvas(master, width=self.tw, height=self.th, bg='white', relief='solid', bd=bd)
        self.draw_grid()
        self.target = []

    def place(self, px, py):
        self.canvas.place(x=px, y=py)

    def draw_grid(self):
        for i in range(1, self.rows):
            self.canvas.create_line(2, self.bh*i, self.tw+2, self.bh*i, fill='light gray')
        for j in range(1, self.cols):
            self.canvas.create_line(self.bw*j, 2, self.bw*j, self.th+2, fill='light gray')

    def draw_block(self, pos, color):
        self.target.clear()
        for pp in pos:
            x, y = calc_coord(self.bw, self.bh, pp[0], pp[1])
            nx, ny = calc_coord(self.bw, self.bh, pp[0] + 1, pp[1] + 1)
            self.target.append(self.canvas.create_rectangle(x, y, nx, ny, fill=color))

    def redraw_block(self, new_pos, color):
        for block in self.target:
            self.canvas.delete(block)
        self.draw_block(new_pos, color)

    def move(self, x, y):
        for block in self.target:
            self.canvas.move(block, x, y)

    def clear(self):
        self.canvas.delete('all')
        self.draw_grid()