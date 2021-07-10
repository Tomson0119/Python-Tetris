import time


class Timer:
    def __init__(self):
        self.start = time.time()
        self.total = 0

    def tick(self):
        end = time.time()
        elapsed = end - self.start
        if elapsed >= 1:
            self.total += int(elapsed)
            self.start = end

    def formatted_time(self):
        st = ''
        minute = self.total // 60
        if minute < 10:
            st += '0'
        st += str(minute)
        st += ':'
        sec = self.total % 60
        if sec < 10:
            st += '0'
        st += str(sec)
        return st
