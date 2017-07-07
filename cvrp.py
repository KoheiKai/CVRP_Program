#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by Kohei Kai(2017)
#
# 積載量制約付き配送計画問題をPuLPソルバを使って解く

try:
    import csv
except:
    print("This implementation requiares the csv module.")
    exit(0)
try:
    import itertools
except:
    print("This implementation requiares the itertools module.")
    exit(0)
try:
    import matplotlib.pyplot as plt
except:
    print("This implementation requiares the matplotlib module.")
    exit(0)
try:
    import networkx as nx
except:
    print("This implementation requiares the networkx module.")
    exit(0)
try:
    import numpy as np
except:
    print("This implementation requiares the numpy module.")
    exit(0)
try:
    import pandas as pd
except:
    print("This implementation requiares the pandas module.")
    exit(0)
try:
    import pulp
except:
    print("This implementation requiares the pulp module.")
    exit(0)
try:
    import time
except:
    print("This implementation requiares the time module.")
    exit(0)

################################################################################

"""
グラフのリストを作成する
@INPUT:
    None
@OUTPUT:
    X:
    Y:
    N:
    pos:
    G:
"""

def createGraphList():
    X = []
    Y = []
    N = []
    G = nx.Graph()
    pos = {}  #ノードの位置情報格納

    # デポ以外の座標を代入
    for i in range(1, num_client):
        X.append(df.ix[i].x)
        Y.append(df.ix[i].y)

    # ノード番号とノードの座標を格納
    for i in range(num_client):
        N.append(i)
        pos[i] = (df.ix[i].x, df.ix[i].y)

    return(X, Y, N, pos, G)

"""
顧客の距離に基づいたコスト行列を返す
@INPUT:
    None
@OUTPUT:
    arr: Matrix of cost
"""

def createCost():
    dis = []
    arr = np.empty((0, num_client), int)  # 小数点以下を加えるならfloat型

    for i in range(num_client):
        for j in range(num_client):
            x_crd = df.ix[j].x - df.ix[i].x
            y_crd = df.ix[j].y - df.ix[i].y

            dis.append(int(np.sqrt(np.power(x_crd, 2) + np.power(y_crd, 2))))
            if j == num_client - 1:
                arr = np.append(arr, np.array([dis]), axis=0)
                dis = []
    np.savetxt("./output/cost.csv", arr, delimiter=',', fmt='%.2f')
    return arr


def createSubTours():
    subtours = []

    for length in range(2, num_client):
        subtours += itertools.combinations(range(1, num_client), length)
    return subtours


def setProblem(capacity):
    x = np.array([[pulp.LpVariable("{0}_{1}".format(i, j), 0, 1, "Binary")
                   for j in range(num_client)]
                  for i in range(num_client)])
    num_v = pulp.LpVariable("num_v", 0, 100, "Integer")  #トラック台数

    problem = pulp.LpProblem('vrp_simple_problem', pulp.LpMinimize)
    problem += pulp.lpSum([x[i][j]*cost[i][j]
                           for i in range(num_client)
                          for j in range(num_client)])

    for t in range(num_client):
        problem += x[t][t] == 0

    for t in range(1, num_client):
        problem += pulp.lpSum(x[:, t]) == 1
        problem += pulp.lpSum(x[t, :]) == 1

    problem += pulp.lpSum(x[:, 0]) == num_v
    problem += pulp.lpSum(x[0, :]) == num_v

    # for edge in not_route:
    #     cant_edge =[]
    #     for i, j in itertools.permutations(edge, 2):
    #         problem += x[i][j] == 0

    print("計算中")
    count = 0
    for st in subtours:
        arcs = []
        demand = 0

        for s in st:
            demand += df["d"][s]
        for i, j in itertools.permutations(st, 2):
            arcs.append(x[i][j])
        is_demand = demand/capacity
        problem += pulp.lpSum(arcs) <= np.max([0, len(st) - np.ceil(is_demand)])
        # count += 1
        # problem += pulp.lpSum(arcs) <= len(st) - 1

    start = time.time()
    # 計算及び結果の確認
    status = problem.solve()
    print("Status", pulp.LpStatus[status])

    elapsed_time = time.time() - start
    print("計算時間：" + str(elapsed_time) + "[sec]")
    print("トラック台数：" + str(num_v.value()) + "台")

    return(x)


def graphPlot(G, N, x):
    E = []
    edge_labels = {}
    sum_cost = 0
    labels = {}

    for i in range(num_client):
        for j in range(num_client):
            if(x[i][j].value() == 1.0):
                sum_cost += cost[i][j]
                print(i, j, x[i][j].value())
                E.append((i, j))
                edge_labels[(i, j)] = cost[i][j]

    print("総移動コスト" + str(sum_cost))

    for i in range(num_client):
        labels[i] = df.ix[i].d


    G.add_nodes_from(N)
    G.add_edges_from(E)
    nx.draw_networkx(G, pos, with_labels=False, node_color='r', node_size=200)
    nx.draw_networkx_labels(G, pos, labels, font_size=12)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.legend()
    plt.xlabel("x")
    plt.ylabel("y")
    plt.xlim(0, 70)
    plt.ylim(0, 70)
    # plt.axis('off')
    plt.title('Delivery route')
    plt.savefig("./fig/cvrp.png")  # save as png
    plt.grid()
    plt.show()

    return(0)


# メイン関数
if __name__ == '__main__':
    capacity = 100  # トラック容量
    filepath = "./data/"  # ファイルパス

    df = pd.read_csv(filepath + "data_r101.csv")
    # num_client = len(df.index)
    num_client = 10  #避難所数設定
    # not_route = {(),()}

    X, Y, N, pos, G = createGraphList()  #グラフ描画準備

    cost = createCost()  #コスト行列作成

    subtours = createSubTours()  #デポ以外の顧客の全部分集合作成

    x = setProblem(capacity)

    graphPlot(G, N, x)
