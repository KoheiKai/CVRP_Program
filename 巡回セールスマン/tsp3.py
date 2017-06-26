# coding: utf-8
#
# tsp3.py : 巡回セールスマン問題 (分割統治法)
#
#           Copyright (C) 2012 Makoto Hiroi
#
import sys
import math
import time
from Tkinter import *

# 標準入力よりデータを読み込む
def read_data():
    buff = []
    for a in sys.stdin:
        b = a.split()
        buff.append((int(b[0]), int(b[1])))
    return buff

# 距離の計算
def distance(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return math.sqrt(dx * dx + dy * dy)

# 経路の距離を求める
def path_length(path):
    global distance_table
    n = 0
    i = 1
    for i in xrange(1, len(path)):
        n += distance(path[i - 1], path[i])
    n += distance(path[0], path[-1])
    return n

# 分割する方向を決定する
def divide_direction(buff):
    x1 = min(map(lambda x: x[0], buff))
    y1 = min(map(lambda x: x[1], buff))
    x2 = max(map(lambda x: x[0], buff))
    y2 = max(map(lambda x: x[1], buff))
    return x2 - x1 > y2 - y1

# 分割する
def divide(buff, comp):
    buff.sort(comp)
    n = len(buff) / 2
    buff1 = buff[:(n+1)]
    buff2 = buff[n:]
    return buff[n], buff1, buff2

# 差分を計算する
def differ(p, c, q):
    return distance(p, c) + distance(c, q) - distance(p, q)

# 共有点を探す
def search(x, buff):
    for i in xrange(len(buff)):
        if buff[i] == x:
            if i == 0: return len(buff) - 1, i, i + 1
            if i == len(buff) - 1: return i - 1, i, 0
            return i - 1, i, i + 1

# 挿入するための新しい経路を作る
def make_new_path(buff, c, succ):
    path = []
    i = c + succ
    while True:
        if i < 0: i = len(buff) - 1
        elif i >= len(buff): i = 0
        if i == c: break
        path.append(buff[i])
        i += succ
    return path

# 併合する
# buff1 = [a, b, c, d, e]
# buff2 = [f, g, c, h, i]
# (1) b - g => [a, b, g, f, i, h, c, d, e]
# (2) d - h => [a, b, c, g, f, i, h, d, e]
# (3) b - h => [a, b, h, i, f. g. c, d, e]
# (4) d - g => [a, b. c. h, i, f, g, d, e]
def merge(buff1, buff2, p):
    # 共有ポイントを探す
    p1, i1, n1 = search(p, buff1)
    p2, i2, n2 = search(p, buff2)
    # 差分を計算
    d1 = differ(buff1[p1], p, buff2[p2])
    d2 = differ(buff1[n1], p, buff2[n2])
    d3 = differ(buff1[p1], p, buff2[n2])
    d4 = differ(buff1[n1], p, buff2[p2])
    # 差分が一番大きいものを選択
    d = max(d1, d2, d3, d4)
    if d1 == d:
        # (1)
        buff1[i1:i1] = make_new_path(buff2, i2, -1)
    elif d2 == d:
        # (2)
        buff1[n1:n1] = make_new_path(buff2, i2, -1)
    elif d3 == d:
        # (3)
        buff1[i1:i1] = make_new_path(buff2, i2, 1)
    else:
        # (4)
        buff1[n1:n1] = make_new_path(buff2, i2, 1)
    return buff1

# 分割統治法による解法
def divide_merge(buff):
    if len(buff) <= 3:
        # print buff
        return buff
    else:
        if divide_direction(buff):
            p, b1, b2 = divide(buff, lambda x, y: x[0] - y[0])
        else:
            p, b1, b2 = divide(buff, lambda x, y: x[1] - y[1])
        b3 = divide_merge(b1)
        b4 = divide_merge(b2)
        return merge(b3, b4, p)

# テスト
def divide_test(buff):
    if len(buff) <= 3:
        print buff
        draw_path(buff)
    else:
        if divide_direction(buff):
            p, b1, b2 = divide(buff, lambda x, y: x[0] - y[0])
        else:
            p, b1, b2 = divide(buff, lambda x, y: x[1] - y[1])
        divide_test(b1)
        divide_test(b2)

# データ入力
point_table = read_data()

s = time.clock()
path = divide_merge(point_table)
e = time.clock()
print path_length(path)
print e - s

# 経路の表示
def draw_path(path):
    x0, y0 = path[0]
    for i in xrange(1, len(path)):
        x1, y1 = path[i]
        c0.create_line(x0, y0, x1, y1)
        x0, y0 = x1, y1
    c0.create_line(x0, y0, path[0][0], path[0][1])
    for x, y in path:
        c0.create_oval(x - 4, y - 4, x + 4, y + 4, fill = "green")

max_x = max(map(lambda x: x[0], point_table)) + 20
max_y = max(map(lambda x: x[1], point_table)) + 20
root = Tk()
c0 = Canvas(root, width = max_x, height = max_y, bg = "white")
c0.pack()

draw_path(path)

root.mainloop()