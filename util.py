def accumulate_delta(delta, max_val, val):
    move = 0
    delta += val
    if val > 0 and delta >= max_val:
        delta = 0
        move = 1
    elif val < 0 and abs(delta) >= max_val:
        delta = 0
        move = -1
    return delta, move


def calc_coord(w, h, r, c):
    return w * c, h * r


def sub_coord(a, b):
    return a[0] - b[0], a[1] - b[1]
