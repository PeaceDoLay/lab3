import math
import random
import sys

import pandas as pd
import numpy as np

from matplotlib import pyplot as plt

print("Введите название файла:")
path = str(input())

columns = pd.read_table(path, delim_whitespace=True, names=['X', 'Y'])

plt.scatter(columns['X'].to_numpy(), columns['Y'].to_numpy())
plt.savefig('output/init_data.png')

print("Введите количество кластеров:")
clustersAmount = int(input())

center = [0] * clustersAmount
centerX = [0.0] * clustersAmount
centerY = [0.0] * clustersAmount

# показывает какая точка к какому кластер у принадлежит
cls = [0] * len(columns)

# находим первые центроиды случайным образом
for i in center:
    ind = center.index(i)
    random_index = int(random.randint(0, len(columns)-1))
    while (random_index in center) or (random_index == 0):
        random_index = int(random.randint(0, len(columns) - 1))
    center[ind] = random_index
    centerX[ind] = columns['X'][random_index]
    centerY[ind] = columns['Y'][random_index]

print(centerX)
print(centerY)

# кол-во переходов между кластерами
jumpAmount = 1

# кол-во точек в каждом кластере
clusterLength = [0] * clustersAmount

while jumpAmount > 0:
    jumpAmount = 0
    # ищем принадлежность к кластерам
    i = 0
    clusterLength = [0] * clustersAmount
    for p in cls:
        xi = columns['X'][i]  # коорд точки
        yi = columns['Y'][i]

        pos = 0
        m = sys.float_info.max
        mini = 0
        for pt in center:
            # расстояние от точки до центров кластера
            distance = math.sqrt(math.pow(xi - centerX[pos], 2) + math.pow(yi - centerY[pos], 2))
            if distance < m:
                m = distance
                mini = pos
            pos += 1
        # увеличиваем кол-во переходов если новое значение кластера не равно прошлому
        if cls[i] != mini:
            jumpAmount += 1
        cls[i] = mini
        clusterLength[mini] += 1
        i += 1
    print(jumpAmount)

    # ищем новые центроиды
    i = 0
    for p in center:
        kc = 0.0
        sumx = 0.0
        sumy = 0.0

        pos = 0
        for pt in cls:
            if pt == i:
                kc += 1.0
                sumx += columns['X'][pos]
                sumy += columns['Y'][pos]
            pos += 1

        centerX[i] = sumx / kc
        centerY[i] = sumy / kc
        i += 1

print(clusterLength)
print(sum(clusterLength))

plt.clf()
i = 0
for pt in center:
    xn = []
    yn = []
    pos = 0
    for p in cls:
        if p == i:
            xn.append(columns['X'][pos])
            yn.append(columns['Y'][pos])
        pos += 1

    plt.scatter(xn, yn)
    i += 1

plt.savefig('output/result.png')

# среднее расстояние от точек до центроида по каждому кластеру
avgDistance = []
i = 0
for pt in center:
    generalDistance = 0.0
    pos = 0
    for p in cls:
        if p == i:
            distance = math.sqrt(math.pow(columns['X'][pos] - centerX[i], 2) + math.pow(columns['Y'][pos] - centerY[i], 2))
            generalDistance += distance
        pos += 1
    generalDistance /= clusterLength[i]
    avgDistance.append(generalDistance)
    i += 1

print(avgDistance)

fig, ax = plt.subplots()
ox = np.arange(len(center))
ax.bar(ox, height=avgDistance)
ax.set_title("Среднее отклонение от центроидов кластера")
fig.savefig('output/avgDistance.png')