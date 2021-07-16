import random
from canvas import *


class Block:
    # 1: I, 2: S, 3: Z, 4: T, 5: L, 6: J, 7: O
    #  0  1  2  3
    #  4  5  6  7
    #  8  9 10 11
    # 12 13 14 15
    SHAPE = {1: [12, 13, 14, 15, 'skyblue'], 2: [10, 11, 13, 14, 'green'],
             3: [9, 10, 14, 15, 'red'], 4: [10, 13, 14, 15, 'purple'],
             5: [11, 13, 14, 15, 'orange'], 6: [9, 13, 14, 15, 'blue'],
             7: [10, 11, 14, 15, 'yellow']}

    def __init__(self):
        self.shape = Block.SHAPE[random.randint(1, 7)]
        self.pos = []
        for n in self.shape[:-1]:
            row = n // 4
            col = n % 4
            self.pos.append([row, col])
        self.stacked = False

    def move_coord(self, dx, dy):
        for p in self.pos:
            p[0] += dy
            p[1] += dx

    def get_bottom(self):
        max_row = max(self.pos, key=lambda p: p[0])[0]
        return [[r, c] for r, c in self.pos if r == max_row]

    @property
    def color(self):
        return self.shape[4]


class Logic:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height + 4)]

    def update(self, block):
        if block and block.stacked:
            for p in block.pos:
                self.board[p[0]+4][p[1]] = 1

    def check_board(self, curr, dx, dy):
        for p in curr:
            nr = p[0] + dy
            nc = p[1] + dx
            if nr >= self.height or \
                    nc < 0 or nc >= self.width or \
                    self.board[nr+4][nc] == 1:
                return False
        return True


class Board:
    def __init__(self, master, size, block_size, row, col):
        self.rows = row
        self.cols = col
        self.bw, self.bh = block_size

        self.dx = 0
        self.dy = 0
        self.df = 0  # Fall
        self.mx, self.my = 0, 0

        self.movable = None
        self.canvas = MyCanvas(master, size, block_size, row, col, 2)

        self.logic = Logic(col, row)
        self.debug = DebugWin(master, self.logic.board)

        self.pressed = {'Left': False, 'Right': False, 'Down': False}

    def place(self, x, y):
        self.canvas.place(x, y)

    def insert(self, block):
        self.movable = block
        self.movable.move_coord(3, -4)
        self.canvas.draw_block(self.movable.pos, block.color)

    def fall(self, dy):
        if self.movable:
            self.df, y = accumulate_delta(self.df, self.bh, dy)
            if self.logic.check_board(self.movable.pos, 0, y):
                self.canvas.move(0, y * self.bh)
                self.movable.move_coord(0, y)
            else:
                self.movable.stacked = True

    def move_block(self, dx, dy):
        if self.movable:
            self.dx, x = accumulate_delta(self.dx, self.bw, dx)
            self.dy, y = accumulate_delta(self.dy, self.bh, dy)
            if self.logic.check_board(self.movable.pos, x, y):
                self.canvas.move(x*self.bw, y*self.bh)
                self.movable.move_coord(x, y)

    def process_key(self, key, pressed):
        if pressed:
            if key == 'Left' and not self.pressed[key]:
                self.pressed[key] = True
                self.mx -= 1
            if key == 'Right' and not self.pressed[key]:
                self.pressed[key] = True
                self.mx += 1
            if key == 'Down' and not self.pressed[key]:
                self.pressed[key] = True
                self.my = 1

        else:
            if key == 'Left' and self.pressed[key]:
                self.pressed[key] = False
                self.mx += 1
            if key == 'Right' and self.pressed[key]:
                self.pressed[key] = False
                self.mx -= 1
            if key == 'Down' and self.pressed[key]:
                self.pressed[key] = False
                self.my = 0

    def is_stacked(self):
        return True if not self.movable else self.movable.stacked

    def update(self, elapsed):
        self.move_block(self.mx * 800 * elapsed, self.my * 600 * elapsed)
        self.logic.update(self.movable)
        self.debug.update(self.logic.board)


class DebugWin:
    def __init__(self, master, board):
        self.win = tk.Toplevel(master)
        self.win.geometry('500x1000')
        self.win.resizable(False, False)
        self.win.title('DEBUG')
        self.win.protocol('WM_DELETE_WINDOW', self.disable_quit)

        self.rows = len(board)
        self.cols = len(board[0])

        self.canvas = MyCanvas(self.win, (396, 960), (40, 40), self.rows, self.cols)
        self.canvas.place(10, 10)

    def disable_quit(self, event=None):
        pass

    def update(self, board):
        self.canvas.clear()
        self.canvas.canvas.create_line(2, 160, 402, 160, width=2)
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 1:
                    self.canvas.draw_block([[i, j]], 'gray')
