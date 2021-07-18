import tkinter as tk
from util import *


class MyCanvas:
    def __init__(self, master, size, block_size, row, col, bd=1):
        self.tw, self.th = size
        self.bw, self.bh = block_size
        self.rows, self.cols = row, col

        self.color = None

        self.canvas = tk.Canvas(master, width=self.tw, height=self.th, bg='white', relief='solid', bd=bd)
        self.draw_grid()

        self.target = []
        self.preview = []
        self.blocks = [[None]*self.cols for _ in range(self.rows)]

    def place(self, px, py):
        self.canvas.place(x=px, y=py)

    def draw_grid(self):
        for i in range(1, self.rows):
            self.canvas.create_line(2, self.bh*i, self.tw+2, self.bh*i, fill='light gray')
        for j in range(1, self.cols):
            self.canvas.create_line(self.bw*j, 2, self.bw*j, self.th+2, fill='light gray')

    def draw_block(self, pos, color, preview=None):
        self.color = color
        self.target.clear()
        for pp in pos:
            x, y = calc_coord(self.bw, self.bh, pp[0], pp[1])
            nx, ny = calc_coord(self.bw, self.bh, pp[0] + 1, pp[1] + 1)
            rect = self.canvas.create_rectangle(x, y, nx, ny, fill=color)
            self.target.append(rect)
            self.blocks[pp[0]][pp[1]] = rect

        if preview:
            self.draw_block_border(preview)

    def draw_block_border(self, pos):
        self.preview.clear()
        for pp in pos:
            x, y = calc_coord(self.bw, self.bh, pp[0], pp[1])
            nx, ny = calc_coord(self.bw, self.bh, pp[0] + 1, pp[1] + 1)
            self.preview.append(self.canvas.create_rectangle(x, y, nx, ny, fill='', outline=self.color, width=2))

    def redraw_block(self, new_pos):
        for block in self.target:
            self.canvas.delete(block)
        self.draw_block(new_pos, self.color)

    def redraw_prev(self, new_pos):
        self.delete_preview()
        self.draw_block_border(new_pos)

    def delete_preview(self):
        for prev in self.preview:
            self.canvas.delete(prev)

    def move(self, x, y, view=None):
        for block, prev in zip(self.target, self.preview):
            self.canvas.move(block, x, y)
            self.canvas.tag_raise(block)
        if view:
            self.redraw_prev(view)

    def move_line(self, src, dst):
        for block in self.blocks[src]:
            self.canvas.move(block, 0, self.bh*(dst-src))

    def clear(self):
        self.canvas.delete('all')
        self.draw_grid()