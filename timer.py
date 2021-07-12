import time


class Timer:
    def __init__(self):
        self.base = 0
        self.total = 0
        self.elapsed = 0
        self.prev = 0
        self.curr = 0
        self.stop = 0
        self.paused = 0
        self.stopped = False

        self.reset()

    def reset(self):
        curr_time = time.time()
        self.base = curr_time
        self.prev = curr_time
        self.stop = 0
        self.stopped = False

    def start(self):
        curr_time = time.time()
        if self.stopped:
            self.paused += (curr_time - self.stop)
            self.prev = curr_time
            self.stop = 0
            self.stopped = False

    def pause(self):
        if not self.stopped:
            curr_time = time.time()
            self.stop = curr_time
            self.stopped = True

    def tick(self):
        if self.stopped:
            self.elapsed = 0
            return

        self.curr = time.time()
        self.elapsed = self.curr - self.prev
        self.prev = self.curr

        if self.elapsed < 0:
            self.elapsed = 0

    def get_elapsed(self):
        return self.elapsed

    def get_total(self):
        if self.stopped:
            return self.stopped - self.base - self.paused
        else:
            return self.curr - self.base - self.paused

    def formatted(self):
        total = int(self.get_total())
        st = ''
        minute = total // 60
        if minute < 10:
            st += '0'
        st += str(minute)
        st += ':'
        sec = total % 60
        if sec < 10:
            st += '0'
        st += str(sec)
        return st
