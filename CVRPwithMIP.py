
import pulp
import pandas as pd
import numpy as np
import networkx as nx
import itertools
import matplotlib.pyplot as plt
import time
import csv


f=open("output.csv", "ab")
csvwriter = csv.writer(f)

#num_client = 15 #顧客数（id=0,1,2,...14と番号が振られていると考える。id=0はデポ。）
capacity = 40 #トラックの容量
randint = np.random.randint

df = pd.read_csv("data_r101.csv")
#num_client = len(df.index) #顧客数（id=0,1,2,...14と番号が振られていると考える。id=0はデポ。）
num_client = 12  #ここで避難所数調整


print(num_client)
print(df)


"""
# 各顧客のx,y座標と需要（どのくらいの商品が欲しいか）をDataFrameとして作成
df = pd.DataFrame({"x":randint(0,100,num_client),
                   "y":randint(0,100,num_client),
                   "d":randint(5,40,num_client)})
#0番目の顧客はデポ（拠点）とみなす。なので、需要=0, 可視化の時に真ん中に来るよう、
#x,yを50に。
df.ix[0].x = 50
df.ix[0].y = 50
df.ix[0].d = 0
"""


#描画用リストに顧客の位置情報を代入
X=[]
Y=[]
for i in range(1, num_client):
    X.append(df.ix[i].x)
    Y.append(df.ix[i].y)



G = nx.Graph()

N = []
for i in range(num_client):
    N.append(i)
    #N.append(df.ix[i].d)

pos = {}
for position in range(num_client):
    pos[position] = (df.ix[position].x,df.ix[position].y )


#全ての顧客間の距離テーブルを作成して、np.arrayを返す。
def create_cost():
    dis = []
    arr = np.empty((0,num_client), int)#小数点以下を加えるならfloat型
    for i in range(num_client):
        for j in range(num_client):
            x_crd = df.ix[j].x - df.ix[i].x
            y_crd = df.ix[j].y - df.ix[i].y

            dis.append(int(np.sqrt(np.power(x_crd,2) + np.power(y_crd,2))))
            if j == num_client-1:
                arr = np.append(arr, np.array([dis]), axis=0)
                dis = []
    np.savetxt("cost.csv",arr, delimiter=',', fmt='%.2f')
    return arr



# costは顧客数✖️顧客数の距離テーブル。np.arrayで保持。  
cost = create_cost()

# subtoursはデポ（id=0)を除いた顧客の全部分集合。
subtours = []
for length in range(2,num_client):
     subtours += itertools.combinations(range(1,num_client),length)

#print(subtours)


# xは顧客数✖️顧客数のbinary変数Array。Costテーブルと対応している。1ならばその間をトラックが走ることになる。
# num_vは必要なトラック台数変数。
x = np.array([[pulp.LpVariable("{0}_{1}".format(i,j),0,1,"Binary")
               for j in range(num_client)]
              for i in range(num_client)])
num_v = pulp.LpVariable("num_v",0,100,"Integer")


#問題の宣言と目的関数設定。目的関数は、総距離最小化。
problem = pulp.LpProblem('vrp_simple_problem', pulp.LpMinimize)
problem += pulp.lpSum([x[i][j]*cost[i][j]
                       for i in range(num_client)
                      for j in range(num_client)])

# 顧客1から顧客1に移動といった結果は有り得ないので除外
for t in range(num_client):
    problem += x[t][t] == 0

# 顧客から出て行くアーク（トラック）と入っていくアーク（トラック）はそれぞれ必ず１本
for t in range(1,num_client):
    problem += pulp.lpSum(x[:,t]) == 1
    problem += pulp.lpSum(x[t,:]) == 1

# デポ（ここでは、id=0)に入ってくるアーク（トラック）と出て行くアーク（トラック）の本数は必ず一緒。
problem += pulp.lpSum(x[:,0]) == num_v
problem += pulp.lpSum(x[0,:]) == num_v


print("計算中")

# ここは肝。上記までの制約だと、デポに戻らない孤立閉路が出来てしまう。ここでやっているのは、
# subtour eliminate制約。さらに、需要も見て、ここでCapacity制約も追加している。興味がある
# 方は、subtour eliminateで検索してください。
for st in subtours:
    arcs = []
    demand = 0

    for s in st:
        demand += df["d"][s]
    for i,j in itertools.permutations(st,2):
        arcs.append(x[i][j])
    problem += pulp.lpSum(arcs) <= np.max([0,len(st) - np.ceil(demand/capacity)])
    #problem += pulp.lpSum(arcs) <= len(st) - 1
    #problem += pulp.lpSum(demand) <= capacity


print("顧客数：" + str(num_client-1))
print("トラック容量：" + str(capacity))

#print(df)
print(cost)
#print(x)


E = []
edge_labels = {}

start = time.time()
#計算及び結果の確認
status = problem.solve()
print("Status", pulp.LpStatus[status])

elapsed_time = time.time() - start
print("計算時間：" + str(elapsed_time) + "[sec]")

sum_cost = 0
for i in range(num_client):
    for j in range(num_client):
        if(x[i][j].value() == 1.0):
            sum_cost += cost[i][j]
            print(i,j,x[i][j].value())
            E.append((i,j))
            edge_labels[(i,j)] = cost[i][j]

print("トラック台数：" + str(num_v.value()) + "台")
print("総移動コスト" + str(sum_cost))


"""
plt.scatter(df.ix[0].x, df.ix[0].y, s= 400, c="yellow", marker="*", alpha=0.5, linewidths="2", edgecolors="orange", label="depot")
plt.plot(X, Y, "o")
plt.legend()
plt.xlabel("x")
plt.ylabel("y")
plt.xlim(0, 100)
plt.ylim(0, 100)
plt.title("CVRPwithMIP")
plt.grid()
plt.show()
"""

#print("------problem----")
#print(problem)

labels = {}
for i in range(num_client):
    labels[i] = df.ix[i].d


G.add_nodes_from(N)
G.add_edges_from(E)

nx.draw_networkx(G,pos,with_labels=False,node_color='r', node_size=150)
nx.draw_networkx_labels(G,pos,labels, font_size=12)
nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels, font_size=8)

plt.legend()
plt.xlabel("x")
plt.ylabel("y")
plt.xlim(0, 70)
plt.ylim(0, 70)
#plt.axis('off')
plt.title('CVRP with MIP')
plt.savefig("cvrp.png") # save as png
plt.grid()
plt.show() 