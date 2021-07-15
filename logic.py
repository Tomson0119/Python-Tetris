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
        self.coord = []
        for n in self.shape[:-1]:
            row = n // 4
            col = n % 4
            self.coord.append([row, col])

    def move_coord(self, dx, dy):
        for p in self.coord:
            p[0] += dy
            p[1] += dx

    def get_bottom(self):
        max_row = max(self.coord, key=lambda p: p[0])[0]
        return [[r, c] for r, c in enumerate(self.coord) if r == max_row]

    @property
    def pos(self):
        return self.coord

    @property
    def color(self):
        return self.shape[4]


class Logic:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]

    def update(self):
        pass

    def check_board(self, curr, dx, dy):
        for p in curr:
            nr = p[0] + dx
            nc = p[1] + dy
            if nr < 0 or nr >= self.height:
                return False
            if nc < 0 or nc >= self.width:
                return False
            if nr == 1 or nc == 1:
                return False
        return True


class Board:
    def __init__(self, master, size, block_size, row, col):
        self.rows = row
        self.cols = col
        self.bw, self.bh = block_size

        self.dx = 0
        self.dy = 0

        self.previous = None
        self.movable = None
        self.canvas = MyCanvas(master, size, block_size, row, col, 2)

        self.logic = Logic(col, row + 4)
        self.debug = DebugWin(master, self.logic.board)

    def place(self, x, y):
        self.canvas.place(x, y)

    def insert(self, block):
        self.movable = block
        self.movable.move_coord(3, -2)
        self.canvas.draw_block(self.movable.pos, block.color)

    def accumulate_delta(self, dx, dy):
        self.dx += dx
        self.dy += dy
        move_x, move_y = 0, 0
        if self.dx >= self.bw:
            self.dx = 0
            move_x = 1
        if self.dy >= self.bh:
            self.dy = 0
            move_y = 1
        return move_x, move_y

    def move_block(self, dx, dy):
        if self.movable:
            x, y = self.accumulate_delta(dx, dy)
            bottom = self.movable.get_bottom()
            if self.logic.check_board(bottom, x, y):
                self.canvas.move(x * self.bw, y * self.bh)
                self.movable.move_coord(x, y)

    def update(self):
        self.logic.update()
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

        self.canvas = MyCanvas(self.win, (400, 960), (40, 40), self.rows, self.cols)
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
