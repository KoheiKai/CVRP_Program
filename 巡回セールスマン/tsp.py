# coding: utf-8
#
# tsp.py : 巡回セールスマン問題
#
#          Copyright (C) 2012 Makoto Hiroi
#
import sys
import math
import time
from pqueue import Queue
from unionfind import *
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

# 経路の長さ
def path_length(path):
    global distance_table
    n = 0
    i = 1
    for i in xrange(1, len(path)):
        n += distance_table[path[i - 1]][path[i]]
    n += distance_table[path[0]][path[-1]]
    return n

###
### 局所探索法
###

# 2-opt 法
def opt_2(size, path):
    global distance_table
    total = 0
    while True:
        count = 0
        for i in xrange(size - 2):
            i1 = i + 1
            for j in xrange(i + 2, size):
                if j == size - 1:
                    j1 = 0
                else:
                    j1 = j + 1
                if i != 0 or j1 != 0:
                    l1 = distance_table[path[i]][path[i1]]
                    l2 = distance_table[path[j]][path[j1]]
                    l3 = distance_table[path[i]][path[j]]
                    l4 = distance_table[path[i1]][path[j1]]
                    if l1 + l2 > l3 + l4:
                        # つなぎかえる
                        new_path = path[i1:j+1]
                        path[i1:j+1] = new_path[::-1]
                        count += 1
        total += count
        if count == 0: break
    return path, total

# or-opt 法 (簡略版)
def or_opt(size, path):
    global distance_table
    total = 0
    while True:
        count = 0
        for i in xrange(size):
            # i 番目の都市を (j) - (j1) の経路に挿入する
            i0 = i - 1
            i1 = i + 1
            if i0 < 0: i0 = size - 1
            if i1 == size: i1 = 0
            for j in xrange(size):
                j1 = j + 1
                if j1 == size: j1 = 0
                if j != i and j1 != i:
                    l1 = distance_table[path[i0]][path[i]]  # i0 - i - i1
                    l2 = distance_table[path[i]][path[i1]]
                    l3 = distance_table[path[j]][path[j1]]  # j - j1
                    l4 = distance_table[path[i0]][path[i1]] # i0 - i1
                    l5 = distance_table[path[j]][path[i]]   # j - i - j1
                    l6 = distance_table[path[i]][path[j1]] 
                    if l1 + l2 + l3 > l4 + l5 + l6:
                        # つなぎかえる
                        p = path[i]
                        path[i:i + 1] = []
                        if i < j:
                            path[j:j] = [p]
                        else:
                            path[j1:j1] = [p]
                        count += 1
        total += count
        if count == 0: break
    return path, total

# 組み合わせ
def optimize1(size, path):
    while True:
        path, _ = opt_2(size, path)
        path, flag = or_opt(size, path)
        if flag == 0: return path

def optimize2(size, path):
    while True:
        path, _ = or_opt(size, path)
        path, flag = opt_2(size, path)
        if flag == 0: return path

###
### 単純な欲張り法 (Nearest Neighbor 法)
###
def greedy0(path):
    global distance_table
    size = len(path)
    for i in xrange(size - 1):
        min_len = 1000000
        min_pos = 0
        for j in xrange(i + 1, size):
            l = distance_table[path[i]][path[j]]
            if l < min_len:
                min_len = l
                min_pos = j
        path[i + 1], path[min_pos] = path[min_pos], path[i + 1]
    return path

###
### クラスカルのアルゴリズムの変形版
###

# 辺の定義
class Edge:
    def __init__(self, p1, p2, weight):
        self.p1 = p1
        self.p2 = p2
        self.weight = weight

    def __cmp__(x, y):
        return x.weight - y.weight

# 辺のデータを作成
def make_edge(size):
    global distance_table
    edges = PQueue()
    for i in xrange(0, size - 1):
        for j in xrange(i + 1, size):
            e = Edge(i, j, distance_table[i][j])
            edges.push(e)
    return edges

# 辺から経路へ
def edge_to_path(edges, size):
    def search_edge(x):
        r = []
        for i in xrange(size):
            if edges[i].p1 == x:
                r.append(edges[i].p2)
            elif edges[i].p2 == x:
                r.append(edges[i].p1)
        return r
    #
    path = [0] * size
    for i in xrange(size - 1):
        x, y = search_edge(path[i])
        if i == 0:
            path[i + 1] = x
            path[-1] = y
        elif path[i - 1] == x:
            path[i + 1] = y
        else:
            path[i + 1] = x
    return path

# 探索
def greedy1(size):
    edges = make_edge(size)
    edge_count = [0] * size
    u = UnionFind(size)
    i = 0
    select_edge = []
    while i < size:
        e = edges.pop()
        if edge_count[e.p1] < 2 and edge_count[e.p2] < 2 and (u.find(e.p1) != u.find(e.p2) or i == size - 1):
            u.union(e.p1, e.p2)
            edge_count[e.p1] += 1
            edge_count[e.p2] += 1
            select_edge.append(e)
            i += 1
    return edge_to_path(select_edge, size)

###
### 分割統治法
###

# 分割する方向を決定する
def divide_direction(buff):
    x1 = min(map(lambda x: point_table[x][0], buff))
    y1 = min(map(lambda x: point_table[x][1], buff))
    x2 = max(map(lambda x: point_table[x][0], buff))
    y2 = max(map(lambda x: point_table[x][1], buff))
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
    return distance_table[p][c] + distance_table[c][q] - distance_table[p][q]

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
            p, b1, b2 = divide(buff, lambda x, y: point_table[x][0] - point_table[y][0])
        else:
            p, b1, b2 = divide(buff, lambda x, y: point_table[x][1] - point_table[y][1])
        b3 = divide_merge(b1)
        b4 = divide_merge(b2)
        return merge(b3, b4, p)

###
### データの入力
###
point_table = read_data()
point_size = len(point_table)
distance_table = distance(point_table)

###
### 実行
###
s = time.clock()
if sys.argv[1] == 'tsp1':
    path = greedy0(range(point_size))
elif sys.argv[1] == 'tsp2':
    path = greedy1(point_size)
else:
    path = divide_merge(range(point_size))
print path_length(path)
print time.clock() - s

# 局所探索法 (逐次改善法)
if len(sys.argv) > 2:
    s = time.clock()
    if sys.argv[2] == '2-opt':
        path, _ = opt_2(point_size, path)
    elif sys.argv[2] == 'or-opt':
        path, _ = or_opt(point_size, path)
    elif sys.argv[2] == 'opt1':
        path = optimize1(point_size, path)
    else:
        path = optimize2(point_size, path)
    print path_length(path)
    print time.clock() - s

###
### 経路の表示
###
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