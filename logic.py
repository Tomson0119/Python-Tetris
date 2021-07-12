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

    def get_pos(self):
        ret = []
        lst = self.shape
        for i in range(len(lst)-1):
            row = lst[i] // 4
            col = lst[i] % 4
            ret.append((row, col))
        return ret

    @property
    def color(self):
        return self.shape[4]


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0]*width for _ in range(height)]







