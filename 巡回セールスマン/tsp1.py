# coding: utf-8
#
# tsp1.py : 巡回セールスマン問題 (単純な欲張り法)
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
def distance(ps):
    size = len(ps)
    table = [[0] * size for _ in xrange(size)]
    for i in xrange(size):
        for j in xrange(size):
            if i != j:
                dx = ps[i][0] - ps[j][0]
                dy = ps[i][1] - ps[j][1]
                table[i][j] = math.sqrt(dx * dx + dy * dy)
    return table

# 単純な欲張り法
def greedy0(size):
    global distance_table
    path = range(size)
    for i in xrange(size - 1):
        min_len = 1000000
        min_pos = 0
        for j in xrange(i + 1, size):
            len = distance_table[path[i]][path[j]]
            if len < min_len:
                min_len = len
                min_pos = j
        path[i + 1], path[min_pos] = path[min_pos], path[i + 1]
    return path

# 経路の長さ
def path_length(path):
    global distance_table
    n = 0
    i = 1
    for i in xrange(1, len(path)):
        n += distance_table[path[i - 1]][path[i]]
    n += distance_table[path[0]][path[-1]]
    return n

# データの入力
point_table = read_data()
point_size = len(point_table)
distance_table = distance(point_table)

s = time.clock()
path = greedy0(point_size)
print path_length(path)
print time.clock() - s

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

draw_path(map(lambda x: point_table[x], path))

root.mainloop()