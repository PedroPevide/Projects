#Simula o patrimônio de uma seguradora com parâmetros variáveis descritos abaixo.

import numpy as np
import random
import plotly.graph_objects as go

def geraJ(s, lbd, v, mu):
    taxa = v + s[0]*mu + s[0]*lbd
    p1 = v/taxa
    p2 = s[0]*mu/taxa
    p3 = s[0]*lbd/taxa
    J = random.choices([1, 2, 3], weights=[p1, p2, p3], k=1)[0]
    return J

def testa_valores_acionamento(vi, vf ,step, prob, iters):
    for j in range(vi, vf, step):
        n = 0
        for i in range(iters):
            check, _ = simula_asseguradora(365, 20, 100000, 12 / 365, j, 1, 2 / 30, 1 / 1095, 60)
            n += check
        media = n/iters
        if media <= prob:
            return j
    return "N/A"

def simula_asseguradora(tmax, n, capital, lbd, media_ac, sigma_ac, v, mu, c):

    #tmax: tempo de simulação
    #n: número de clientes no início do período
    #capital: patrimônio inicial da asseguradora
    #lbd: taxa da distribuição da quantidade de ativamentos de seguro
    #media_ac: media do custo incorrido para a asseguradora pelo acionamento do seguro
    #sigma_ac: desvio padrão do custo incorrido para a asseguradora pelo acionamento do seguro
    #v: taxa com que novos clientes contratam o seguro por período de tempo
    #mu: taxa da distribuição de tempo exponencial com que os clientes permanecem assinando o seguro
    #c: custo do plano por unidade de tempo para os clientes.

    hist = [[0], [n], [capital]] #tempo, clientes, patrimonio

    s = [n, capital]
    t = 0

    taxa = v + s[0]*mu + s[0]*lbd
    t_evento = np.random.exponential(1/taxa)

    while True:
        if t_evento > tmax:
            return 1, hist
        else:
            s[1] += s[0]*c*(t_evento - t)
            hist[2].append(s[1])

            t = t_evento
            hist[0].append(t_evento)

            j = geraJ(s, lbd, v, mu)

            match j:
                case 1:
                    s[0] += 1
                    hist[1].append(s[0])
                case 2:
                    s[0] = max(0, s[0] - 1)
                    hist[1].append(s[0])
                case 3:
                    sigma = np.sqrt(np.log(1 + (sigma_ac / media_ac) ** 2))
                    media = np.log(media_ac) - (sigma_ac ** 2) / 2
                    y = np.random.lognormal(media, sigma)
                    if y > s[1]:
                        # print("Asseguradora Endividada")
                        s[1] -= y
                        hist[2][-1] = s[1]
                        return 0, hist
                    else:
                        hist[1].append(s[0])
                        s[1] -= y

            taxa = v + s[0]*mu + s[0]*lbd
            t_evento = t + np.random.exponential(1/taxa)


#------------------------------------------------------------------------------------------------------------------#

iters = 10000
n = 0
patrimonio = 0

for i in range(iters):
    check, hist = simula_asseguradora(365, 20, 100000, 12/365, 3620, 1, 2/30, 1/1095, 60)
    n += check
    patrimonio += hist[2][-1]
print(f"Probabilidade da Seguradora não falir: {n/iters}")
print(f"Patrimônio Médio da Seguradora no Final do Período: {patrimonio/iters}")


#-----------------------------------------------------------------------------------------------------------------#
# check, hist = simula_asseguradora(365, 20, 100000, 12/365, 3250, 1, 2/30, 1/1095, 60)


# fig1 = go.Figure(data=go.Scatter(x=hist[0], y=hist[2], mode='markers+lines'))
# fig1.update_layout(title="Patrimônio da Seguradora em Função do Tempo", xaxis_title="Dias", yaxis_title="Patrimônio")
# fig1.show()
#
# fig2 = go.Figure(data=go.Scatter(x=hist[0], y=hist[1], mode='markers+lines'))
# fig2.update_layout(title="Número de Clientes da Seguradora em Função do Tempo", xaxis_title="Dias", yaxis_title="Nº Clientes")
# fig2.show()
#------------------------------------------------------------------------------------------------------------------#

# prob = 0.25
# acionamento = testa_valores_acionamento(3500, 4000, 10, prob, 5000)
#
# print(f"Valor de acionamento para probabilidade menor ou igual a {prob}: {acionamento}")


