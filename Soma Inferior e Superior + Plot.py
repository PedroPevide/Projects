#Código para plot de somas superiores e inferiores de funções
import numpy as np
import plotly as px
import matplotlib.pyplot as plt

def funcao(x):
    if -3 <= x < 0:
        return 1 - x
    if 0 <= x <= 3:
        return 2 - (x-2)**2/3

def maxs(f_values):
    values = []
    for i in range(len(f_values)-1):
        values.append(max(f_values[i], f_values[i+1]))
    return values
    
def mins(f_values):
    values = []
    for i in range(len(f_values)-1):
        values.append(min(f_values[i], f_values[i+1]))
    return values
    
def soma_inf(f_values, x):
    sum = 0
    for i in range(len(f_values)-1):
        sum += min(f_values[i], f_values[i+1]) * (x[i+1]-x[i])
    return sum

def soma_sup(f_values, x):
    sum = 0
    for i in range(len(f_values)-1):
        sum += max(f_values[i], f_values[i+1]) * (x[i+1]-x[i])
    return sum

x_disc = np.arange(-3, 4, 1)
x_cont = np.arange(-3., 4., 0.01)
f_xdisc = []
f_xcont = []

for i in x_disc:
    f_xdisc.append(funcao(i))

for i in x_cont:
    f_xcont.append(funcao(i))

f_mins = mins(f_xdisc)
f_maxs = maxs(f_xdisc)

plt.plot(x_cont, f_xcont)
plt.title("Soma Inferior")
plt.figtext(0.55, 0.8, f"Área: {soma_sup(f_xdisc, x_disc)}")
for i in range(len(f_xdisc)-1):
    plt.bar(x_disc[i], f_maxs[i], 1, align = 'edge', edgecolor = '0', facecolor = '0.8')
plt.show()