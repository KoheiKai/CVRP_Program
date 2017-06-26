# coding: utf-8
#
# tsp0.py : 巡回セールスマン問題 (深さ優先探索)
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

# 距離をセット
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

# 経路の距離を求める
def path_length(path):
    global distance_table
    n = 0
    i = 1
    for i in xrange(1, len(path)):
        n += distance_table[path[i - 1]][path[i]]
    n += distance_table[path[0]][path[-1]]
    return n

# 単純な深さ優先探索
def dfs(size):
    def dfs_sub(n, path):
        global min_length, min_path
        if size == n:
            new_len = path_length(path)
            if new_len < min_length:
                min_length = new_len
                min_path = path[:]
        else:
            for x in xrange(1, size):
                if x not in path:
                    if n != 2 or path[0] > x:
                        path.append(x)
                        dfs_sub(n + 1, path)
                        path.pop()
    #
    global min_length, min_path
    min_length = 1e100
    min_path = []
    for x in xrange(1, size):
        dfs_sub(2, [x, 0])

# データ入力と大域変数の初期化
point_table = read_data()
distance_table = distance(point_table)

s = time.clock()
dfs(len(point_table))
print min_length
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

draw_path(map(lambda x: point_table[x], min_path))

root.mainloop()
