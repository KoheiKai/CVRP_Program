# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

num_client = 15 #顧客数（id=0,1,2,...14と番号が振られていると考える。id=0はデポ。）
capacity = 100 #トラックの容量
randint = np.random.randint

# 各顧客のx,y座標と需要（どのくらいの商品が欲しいか）をDataFrameとして作成
df = pd.DataFrame({"x":randint(0,100,num_client),
                   "y":randint(0,100,num_client),
                   "d":randint(5,40,num_client)})
#0番目の顧客はデポ（拠点）とみなす。なので、需要=0, 可視化の時に真ん中に来るよう、
#x,yを50に。
df.ix[0].x = 50
df.ix[0].y = 50
df.ix[0].d = 0

X=[]
Y=[]
for i in range(1, num_client):
    X.append(df.ix[i].x)
    Y.append(df.ix[i].y)


plt.scatter(df.ix[0].x, df.ix[0].y, s= 400, c="yellow", marker="*", alpha=0.5, linewidths="2", edgecolors="orange", label="depot")
plt.plot(X, Y, "o")
#plt.hlines([50], 0, 100, linestyles="dashed")
#plt.vlines([50], 0, 100, linestyles="dashed")
plt.legend()
plt.xlabel("x")
plt.ylabel("y")
plt.xlim(0, 100)
plt.ylim(0, 100)
plt.show()