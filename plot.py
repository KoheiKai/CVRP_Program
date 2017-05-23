# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

num_client = 15 #�ڋq���iid=0,1,2,...14�Ɣԍ����U���Ă���ƍl����Bid=0�̓f�|�B�j
capacity = 100 #�g���b�N�̗e��
randint = np.random.randint

# �e�ڋq��x,y���W�Ǝ��v�i�ǂ̂��炢�̏��i���~�������j��DataFrame�Ƃ��č쐬
df = pd.DataFrame({"x":randint(0,100,num_client),
                   "y":randint(0,100,num_client),
                   "d":randint(5,40,num_client)})
#0�Ԗڂ̌ڋq�̓f�|�i���_�j�Ƃ݂Ȃ��B�Ȃ̂ŁA���v=0, �����̎��ɐ^�񒆂ɗ���悤�A
#x,y��50�ɁB
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