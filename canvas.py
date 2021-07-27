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
        self.stacked = [[None]*self.cols for _ in range(self.rows)]

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

        if preview:
            self.draw_block_border(preview)

    def draw_block_border(self, pos):
        self.preview.clear()
        for pp in pos:
            x, y = calc_coord(self.bw, self.bh, pp[0], pp[1])
            nx, ny = calc_coord(self.bw, self.bh, pp[0] + 1, pp[1] + 1)
            self.preview.append(self.canvas.create_rectangle(x, y, nx, ny, fill='', outline=self.color, width=2))

    def redraw_block(self, new_pos):
        self.delete_object(self.target)
        self.draw_block(new_pos, self.color)

    def redraw_prev(self, new_pos):
        self.delete_object(self.preview)
        self.draw_block_border(new_pos)

    def delete_object(self, objects):
        for obj in objects:
            self.canvas.delete(obj)

    def move(self, x, y, view=None):
        for block in self.target:
            self.canvas.move(block, x, y)
            self.canvas.tag_raise(block)
        if view:
            self.redraw_prev(view)

    def add_stacked(self, pos):
        self.delete_object(self.preview)
        for i in range(len(pos)):
            self.stacked[pos[i][0]][pos[i][1]] = self.target[i]

    def drop_line(self, hits):
        i = 0
        for row in range(hits[0], -1, -1):
            if row in hits:
                i += 1
                for col in range(self.cols):
                    self.delete_object(self.stacked[row])
            else:
                for block in self.stacked[row]:
                    if block:
                        self.canvas.move(block, 0, self.bh*i)
                self.stacked[row + i] = self.stacked[row]
            self.stacked[row] = [None] * self.rows


    def clear(self):
        self.canvas.delete('all')
        self.draw_grid()
