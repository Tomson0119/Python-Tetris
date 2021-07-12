import tkinter as tk


class MyCanvas:
    def __init__(self, master, size, block_size, border=1):
        self.tw, self.th = size
        self.bw, self.bh = block_size
        self.rows, self.cols = 0, 0

        self.canvas = tk.Canvas(master, width=self.tw, height=self.th, bg='white', relief='solid', bd=border)

    def place(self, px, py):
        self.canvas.place(x=px, y=py)

    def draw_grid(self, rows, cols):
        self.rows = rows
        self.cols = cols
        for i in range(1, rows):
            self.canvas.create_line(2, self.bh*i, self.tw+2, self.bh*i, fill='light gray')
        for j in range(1, cols):
            self.canvas.create_line(self.bw*j, 2, self.bw*j, self.th+2, fill='light gray')

    def draw_block(self, block):
        color, p = block.color, block.get_pos()
        for pp in p:
            x, y = MyCanvas.calc_coord(self.bw, self.bh, pp[0], pp[1])
            nx, ny = MyCanvas.calc_coord(self.bw, self.bh, pp[0] + 1, pp[1] + 1)
            self.canvas.create_rectangle(x, y, nx, ny, fill=color)

    def clear(self):
        self.canvas.delete('all')
        self.draw_grid(self.rows, self.cols)

    @staticmethod
    def calc_coord(w, h, r, c):
        return w * c, h * r