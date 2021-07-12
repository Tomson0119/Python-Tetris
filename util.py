
def calc_coord(w, h, r, c):
    return w * c, h * r


def move_coord(pos, dx, dy):
    for p in pos:
        p[0] += dx
        p[1] += dy
    return pos
