import random
from canvas import *


class Block:
    #  0  1  2  3
    #  4  5  6  7
    #  8  9 10 11
    # 12 13 14 15
    SHAPE = {1: 'I', 2: 'S', 3: 'Z', 4: 'T', 5: 'L', 6: 'J', 7: 'O'}
    SHAPE_INFO = {'I': [12, 13, 14, 15, 'skyblue'], 'S': [10, 11, 14, 13, 'green'],
                  'Z': [9, 10, 14, 15, 'red'], 'T': [10, 13, 14, 15, 'purple'],
                  'L': [11, 13, 14, 15, 'orange'], 'J': [9, 13, 14, 15, 'blue'],
                  'O': [10, 11, 14, 15, 'yellow']}
    COUNTERCLOCKWISE = {(-1 + i, -1 + j): (2 - i - j, 0 + i - j) for i in range(3) for j in range(3)}
    CLOCKWISE = {(-1 + i, -1 + j): (0 - i + j, 2 - i - j) for i in range(3) for j in range(3)}

    def __init__(self):
        self.shape = Block.SHAPE[random.randint(1, 7)]
        self.info = Block.SHAPE_INFO[self.shape]
        self.color = self.info[4]

        self.pos = []
        for n in self.info[:-1]:
            row = n // 4
            col = n % 4
            self.pos.append([row, col])

        self.vertical = False  # shape: I, S, Z
        self.stacked = False

    def move_coord(self, dx, dy):
        for p in self.pos:
            p[0] += dy
            p[1] += dx

    def rotate_coord(self, delta):
        assert len(delta) == len(self.pos)
        self.vertical = not self.vertical
        for i in range(len(delta)):
            self.pos[i][0] += delta[i][0]
            self.pos[i][1] += delta[i][1]

    def get_bottom_row(self):
        return max(self.pos, key=lambda p: p[0])[0]

    def get_diff(self, val):
        ret = []
        center = self.pos[2]
        for p in self.pos:
            sub = sub_coord(p, center)
            if val:
                ret.append(Block.COUNTERCLOCKWISE[sub])
            else:
                ret.append(Block.CLOCKWISE[sub])
        return ret

    def get_rotate_delta(self, clockwise):
        diff = []
        if self.shape not in ['I', 'S', 'Z']:
            diff = self.get_diff(clockwise)
        elif self.shape in ['S', 'Z']:
            diff = self.get_diff(self.vertical)
        elif self.shape == 'I':
            k = 1 if self.vertical else -1
            for i in range(4):
                diff.append((k*(2 - i), k*(-2 + i)))
        return diff


class Logic:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height + 4)]

    def update(self, block):
        if block and block.stacked:
            for p in block.pos:
                self.board[p[0] + 4][p[1]] = 1

    def check_valid(self, p, dx, dy):
        nr = p[0] + dy
        nc = p[1] + dx
        if nr >= self.height or \
                nc < 0 or nc >= self.width or \
                self.board[nr + 4][nc] == 1:
            return False
        return True

    def check_move(self, curr, dx, dy):
        for p in curr:
            if not self.check_valid(p, dx, dy):
                return False
        return True

    def check_rotate(self, curr, delta):
        assert len(curr) == len(delta)
        center = curr[2]
        adjust_x, adjust_y = 0, 0
        for i in range(len(curr)):
            nr = curr[i][0] + delta[i][0]
            nc = curr[i][1] + delta[i][1]
            if nc < 0:
                adjust_x = 1
            elif nc >= self.width:
                adjust_x = nc - self.width - 1
            elif nr >= self.height:
                adjust_y = nr - self.height - 1

            elif self.board[nr+4][nc] == 1:
                if self.board[nr+4][center[1]] == 1:
                    adjust_y = -1
                elif self.board[center[0]+4][nc] == 1:
                    adjust_x = 1 if center[1] > nc else -1
        return [adjust_x, adjust_y]

    def check_line(self, row):
        for c in range(self.width):
            if self.board[row+4][c] == 0:
                return False
        return True

    def drop_line(self, hits):
        i = 0
        for row in range(hits[0], -1, -1):
            if row in hits:
                i += 1
            else:
                self.board[row+4+i] = self.board[row+4]
            self.board[row + 4] = [0] * self.width


class Board:
    def __init__(self, master, size, block_size, row, col, timer):
        self.rows = row
        self.cols = col
        self.bw, self.bh = block_size

        self.timer = timer

        self.dx = 0
        self.anim_dx = 0
        self.dy = 0
        self.df = 0  # Fall
        self.mx, self.my = 0, 0

        self.movable = None
        self.canvas = MyCanvas(master, size, block_size, row, col, 2)

        self.logic = Logic(col, row)
        self.debug = DebugWin(master, self.logic.board)

        self.pressed = {'Left': False, 'Right': False, 'Down': False, 'z': False, 'x': False, 'c': False}

    def place(self, x, y):
        self.canvas.place(x, y)

    def insert(self, block):
        self.movable = block
        self.movable.move_coord(3, -4)
        self.canvas.draw_block(self.movable.pos, block.color, self.preview_pos())

    def preview_pos(self):
        i = 0
        while True:
            if not self.logic.check_move(self.movable.pos, 0, i):
                i = i - 1
                break
            i += 1
        return [[r+i, c] for r, c in self.movable.pos]

    def fall(self, dy):
        if self.movable:
            self.df, y = accumulate_delta(self.df, self.bh, dy)
            if self.logic.check_move(self.movable.pos, 0, y):
                self.canvas.move(0, y * self.bh)
                self.movable.move_coord(0, y)
            else:
                self.movable.stacked = True

    def move_block(self, dx, dy):
        if self.movable:
            self.dx, x = accumulate_delta(self.dx, self.bw, dx)
            self.dy, y = accumulate_delta(self.dy, self.bh, dy)
            if self.logic.check_move(self.movable.pos, x, y):
                prev_pos = self.preview_pos()
                self.canvas.move(x * self.bw, y * self.bh, prev_pos)
                self.movable.move_coord(x, y)
                if prev_pos == self.movable.pos:
                    self.canvas.add_stacked(self.movable.pos)

    def rotate_block(self, clockwise):
        delta = self.movable.get_rotate_delta(clockwise)
        adjust = self.logic.check_rotate(self.movable.pos, delta)
        self.movable.rotate_coord(delta)
        self.movable.move_coord(*adjust)
        self.canvas.redraw_block(self.movable.pos)

    def instant_move(self):
        prev_pos = self.preview_pos()
        dy = prev_pos[0][0] - self.movable.pos[0][0]
        self.canvas.move(0, dy * self.bh)
        self.movable.move_coord(0, dy)
        self.movable.stacked = True

    def process_key(self, key, pressed):
        if pressed and key in self.pressed.keys() and not self.pressed[key]:
            self.pressed[key] = True
            if key == 'Left':
                self.mx -= 1
            if key == 'Right':
                self.mx += 1
            if key == 'Down':
                self.my = 1
                self.df = 0
            if key == 'z':
                self.rotate_block(clockwise=False)
            if key == 'x':
                self.rotate_block(clockwise=True)
            if key == 'c':
                self.instant_move()

        elif not pressed and key in self.pressed.keys() and self.pressed[key]:
            self.pressed[key] = False
            if key == 'Left':
                self.mx += 1
            if key == 'Right':
                self.mx -= 1
            if key == 'Down':
                self.my = 0

    def delete_curr_block(self):
        self.canvas.delete_object(self.canvas.target)
        self.canvas.delete_object(self.canvas.preview)
        self.movable = None

    def check_lines(self):
        hit_lines = []
        for r in range(self.rows-1, -1, -1):
            if self.logic.check_line(r):
                hit_lines.append(r)
        if hit_lines:
            self.logic.drop_line(hit_lines)
            self.canvas.drop_line(hit_lines)

    def is_stacked(self):
        return True if not self.movable else self.movable.stacked

    def update(self, elapsed):
        self.move_block(self.mx * 800 * elapsed, self.my * 600 * elapsed)
        self.logic.update(self.movable)
        self.check_lines()
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
                    self.canvas.draw_block([[i, j]], 'red')
