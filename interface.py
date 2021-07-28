import timer
import copy

from tkinter import ttk
from tkinter import font

from logic import *


class App:
    def __init__(self):
        self.win = tk.Tk()
        self.win.geometry('685x820')
        self.win.resizable(False, False)
        self.win.title('TETRIS')
        self.win.bind('<KeyPress>', self.key_pressed)
        self.win.bind('<KeyRelease>', self.key_released)

        self.level_label = None
        self.line_label = None
        self.time_label = None
        self.score_label = None
        self.board = None
        self.keep_board = None
        self.next_board = []

        self.level = 1
        self.goal_hit = 10
        self.curr_hit = 0
        self.score = 0
        self.curr_block = None

        self.timer = timer.Timer()
        self.queue = [Block() for _ in range(3)]

        self.build_widgets()
        self.fill_next_boards()

    def build_widgets(self):
        default_font = font.Font(family='Malgun Gothic', size=20)
        style = ttk.Style(self.win)
        style.configure('TLabel', font=default_font)
        style.map('TLabel', background=[(None, 'white')])

        keep_label = ttk.Label(text='KEEP', anchor='center')
        keep_label.place(x=10, y=12, width=120, height=40)

        self.keep_board = MyCanvas(self.win, (117, 117), (30, 30), 4, 4)
        self.keep_board.place(8, 60)

        level_title = ttk.Label(text='LEVEL', anchor='center')
        level_title.place(x=10, y=500, width=120, height=40)
        self.level_label = ttk.Label(text=self.level, anchor='e')
        self.level_label.place(x=10, y=550, width=120, height=40)

        line_title = ttk.Label(text='LINES', anchor='center')
        line_title.place(x=10, y=600, width=120, height=40)
        self.line_label = ttk.Label(text=str(self.curr_hit) + '/' + str(self.goal_hit), anchor='e')
        self.line_label.place(x=10, y=650, width=120, height=40)

        self.board = Board(self.win, (396, 796), (40, 40), 20, 10)
        self.board.place(140, 10)

        next_label = ttk.Label(text='NEXT', anchor='center')
        next_label.place(x=552, y=12, width=120, height=40)
        for i in range(3):
            self.next_board.append(MyCanvas(self.win, (117, 117), (30, 30), 4, 4))
            self.next_board[i].place(550, 60+i*130)

        time_title = ttk.Label(text='TIME', anchor='center')
        time_title.place(x=552, y=500, width=120, height=40)
        self.time_label = ttk.Label(text='00:00', anchor='center')
        self.time_label.place(x=552, y=550, width=120, height=40)

        score_title = ttk.Label(text='SCORE', anchor='center')
        score_title.place(x=552, y=600, width=120, height=40)
        self.score_label = ttk.Label(text=self.score, anchor='e')
        self.score_label.place(x=552, y=650, width=120, height=40)

    def destroy_all(self, event=None):
        self.queue.clear()
        self.win.destroy()

    def fill_next_boards(self):
        for i in range(3):
            pos = self.queue[i].pos
            color = self.queue[i].color
            self.next_board[i].clear()
            self.next_board[i].draw_block(pos, color)

    def keep_block(self):
        if self.curr_block:
            self.keep_board.clear()
            self.keep_board.draw_block(self.curr_block.pos, self.curr_block.color)

    def update(self):
        self.timer.tick()
        text = self.timer.formatted()    # 현재 시간을 문자열로 변환하고
        self.time_label.configure(text=text)  # 레이블을 업데이트한다.

        self.board.fall(self.level*50 * self.timer.get_elapsed())
        self.board.update(self.timer.get_elapsed())

        if self.board.is_stacked():
            self.curr_block = self.queue.pop(0)
            self.board.insert(copy.deepcopy(self.curr_block))
            self.queue.append(Block())  # 큐에 새로운 블록을 넣고
            self.fill_next_boards()  # 캔버스를 다시 그린다.

        self.win.after(1, self.update)

    def key_pressed(self, event=None):
        if event:
            if event.keysym == 'Escape':
                self.destroy_all()
            if event.keysym == 'c':
                self.keep_block()
            else:
                self.board.process_key(event.keysym, True)

    def key_released(self, event=None):
        if event:
            self.board.process_key(event.keysym, False)

    def run(self):
        self.update()
        self.win.mainloop()
