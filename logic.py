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

    @property
    def pos(self):
        ret = []
        lst = self.shape
        for i in range(len(lst)-1):
            row = lst[i] // 4
            col = lst[i] % 4
            ret.append([row, col])
        return ret

    @property
    def color(self):
        return self.shape[4]


class Board:
    def __init__(self, master, size, block_size, width, height):
        self.width = width
        self.height = height
        self.bw, self.bh = block_size

        self.dx = 0
        self.dy = 0

        self.target = [[0, 0] for _ in range(4)]
        self.board = [[0]*width for _ in range(height + 4)]
        self.canvas = MyCanvas(master, size, block_size, 2)
        self.canvas.draw_grid(height, width)

        self.debug = DebugWin(master, self.board)

    def place(self, x, y):
        self.canvas.place(x, y)

    def insert(self, block):
        pos = move_coord(block.pos, -2, 3)
        for i, p in enumerate(pos):
            self.target[i] = [p[0]+4, p[1]]
        self.canvas.draw_block(pos, block.color)

    def accumulate_delta(self, dx, dy):
        self.dx += dx
        self.dy += dy
        move_x, move_y = 0, 0
        if self.dx >= self.bw:
            self.dx = 0
            move_x = self.bw
        if self.dy >= self.bh:
            self.dy = 0
            move_y = self.bh
        return move_x, move_y

    def move(self, dx, dy):
        x, y = self.accumulate_delta(dx, dy)
        self.canvas.move(x, y)

    def update(self):
        for p in self.target:
            self.board[p[0]][p[1]] = 1
        self.debug.update(self.board)

    def print_board(self):
        for lst in self.board:
            for n in lst:
                print(n, end=' ')
            print()


class DebugWin:
    def __init__(self, master, board):
        self.win = tk.Toplevel(master)
        self.win.geometry('500x1000')
        self.win.resizable(False, False)
        self.win.title('DEBUG')
        self.win.protocol('WM_DELETE_WINDOW', self.disable_quit)

        self.rows = len(board)
        self.cols = len(board[0])

        self.canvas = MyCanvas(self.win, (400, 960), (40, 40))
        self.canvas.draw_grid(self.rows, self.cols)
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