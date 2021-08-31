import tkinter as tk
from PIL import ImageTk, Image
from util import *


class MyCanvas:
    def __init__(self, master, size, block_size, row, col, bd=1):
        self.tw, self.th = size
        self.bw, self.bh = block_size
        self.rows, self.cols = row, col

        self.color = None
        self.anim_dx = 0

        self.canvas = tk.Canvas(master, width=self.tw, height=self.th, bg='white', relief='solid', bd=bd)
        self.draw_grid()

        self.target = []
        self.preview = []
        self.hits = []
        self.stacked = [[None]*self.cols for _ in range(self.rows)]

        colors = ['red', 'green', 'orange', 'purple', 'blue', 'skyblue', 'yellow']
        self.photo = {}
        for color in colors:
            image = Image.open('resource/' + color + '.png')
            image = image.resize((self.bw, self.bh))
            self.photo.setdefault(color, ImageTk.PhotoImage(image))

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
            rect = self.canvas.create_image(x, y, anchor='nw', image=self.photo[color])
            self.target.append(rect)

        if preview:
            self.draw_block_border(preview)

    def draw_block_border(self, pos):
        self.preview.clear()
        for pp in pos:
            x, y = calc_coord(self.bw, self.bh, pp[0], pp[1])
            nx, ny = calc_coord(self.bw, self.bh, pp[0] + 1, pp[1] + 1)
            color = self.color if self.color != 'yellow' else 'gold'
            self.preview.append(self.canvas.create_rectangle(x, y, nx, ny, fill='', outline=color, width=2))

    def redraw_block(self, new_pos):
        self.delete_object(self.target)
        self.draw_block(new_pos, self.color)

    def redraw_prev(self, new_pos):
        self.delete_object(self.preview)
        self.draw_block_border(new_pos)

    def delete_object(self, objects):
        for obj in objects:
            self.canvas.delete(obj)
        objects.clear()

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

    def remove_lines(self, hits):
        for row in hits:
            for col in range(self.cols):
                self.delete_object(self.stacked[row])

    def drop_line(self, hits):
        i = 0
        for row in range(hits[0], -1, -1):
            if row in hits:
                i += 1
            else:
                for block in self.stacked[row]:
                    if block:
                        self.canvas.move(block, 0, self.bh*i)
                self.stacked[row + i] = self.stacked[row]
            self.stacked[row] = [None] * self.rows

    def add_hits(self, lines):
        for line in lines:
            x, y = calc_coord(self.bw, self.bh, line, 0)
            nx, ny = calc_coord(self.bw, self.bh, line+1, self.rows)
            self.hits.append(self.canvas.create_rectangle(x, y, nx, ny, fill='light gray', outline='light gray'))

    def animate(self, dx):
        if self.hits:
            for hit in self.hits:
                self.canvas.move(hit, dx, 0)
            self.anim_dx += dx
            if self.anim_dx > self.cols * self.bw:
                self.anim_dx = 0
                self.delete_object(self.hits)
                return True
        return False

    def clear(self):
        self.canvas.delete('all')
        self.draw_grid()
