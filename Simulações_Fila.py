import numpy as np
import plotly.graph_objects as go
from itertools import islice


def gera_ts(s, lambda1):
    t = s
    while True:
        u = np.random.uniform(0, 1)
        t = t - (1/lambda1) * np.log(u)
        u = np.random.uniform(0, 1)
        if u <= 1:
            return t

def simula_filaParalela(tmax, lambda_c, lambda_s1, lambda_s2):

    tmax = tmax
    t = 0
    N = 0
    estados = [0, 0, 0]
    C = {}
    P = {}
    A = {}
    S = {}
    tc = gera_ts(0, lambda_c)
    t1 = np.inf
    t2 = np.inf
    n_clientes = []
    t_clientes = []
    fechado = 0
    restante = 0

    while fechado == 0 or estados[0] > 0:
        if fechado == 0:
            if min(tc, t1, t2) == tc and tc <= tmax:

                t = tc
                N += 1
                tc = gera_ts(t, lambda_c)
                if tc > tmax:
                    fechado = 1
                C[f"Cliente {N}"] = round(float(t), 3)

                A[f"Cliente {N}"] = round(float(t), 3)


                match estados:
                    case [0, 0, 0]:
                        estados = [1, N, 0]
                        n_clientes.append(estados[0])
                        t_clientes.append(round(float(t), 3))
                        t1 = t + np.random.exponential(lambda_s1)
                        if t1 > tmax:
                            restante += 1
                        S[f"Cliente {N}"] = 1
                        continue

                    case [1, _, 0]:
                        estados[0] = 2
                        estados[2] = N
                        n_clientes.append(estados[0])
                        t_clientes.append(round(float(t), 3))
                        t2 = t + np.random.exponential(lambda_s2)
                        if t2 > tmax:
                            restante += 1
                        S[f"Cliente {N}"] = 2
                        continue

                    case [1, 0, _]:
                        estados[0] = 2
                        estados[1] = N
                        n_clientes.append(estados[0])
                        t_clientes.append(round(float(t), 3))
                        t1 = t + np.random.exponential(lambda_s1)
                        if t1 > tmax:
                            restante += 1
                        S[f"Cliente {N}"] = 1
                        continue

                    case [n, *_] if n > 1:
                        estados[0] += 1
                        n_clientes.append(estados[0])
                        t_clientes.append(round(float(t), 3))

                        # for j in range(N-1):
                        #     if j+1 not in (estados[1], estados[2]) and f"Cliente {j+1}" not in P:
                        #         E[f"Cliente {j+1}"] += t


                        continue

            if t1 < tc and t1 <= t2:
                t = t1
                P[f"Cliente {estados[1]}"] = round(float(t), 3)

                match estados:
                    case [1, *_]:
                        estados = [0, 0, 0]
                        n_clientes.append(estados[0])
                        t_clientes.append(round(float(t), 3))
                        t1 = np.inf
                        continue

                    case [2, *_]:
                        estados[0] = 1
                        estados[1] = 0
                        n_clientes.append(estados[0])
                        t_clientes.append(round(float(t), 3))
                        t1 = np.inf
                        continue

                    case [n, *_] if n > 2:
                        m = max(estados[1], estados[2])
                        estados[0] -= 1
                        estados[1] = m + 1

                        A[f"Cliente {m+1}"] = round(float(t), 3)

                        n_clientes.append(estados[0])
                        t_clientes.append(round(float(t), 3))
                        t1 = t + np.random.exponential(lambda_s1)
                        if t1 > tmax:
                            restante += 1
                        S[f"Cliente {m+1}"] = 1
                        continue

            if t2 < tc and t2 < t1:
                t = t2
                P[f"Cliente {estados[2]}"] = round(float(t), 3)

                match estados:
                    case [1, *_]:
                        estados = [0, 0, 0]
                        n_clientes.append(estados[0])
                        t_clientes.append(round(float(t), 3))
                        t2 = np.inf
                        continue

                    case [2, *_]:
                        estados[0] = 1
                        estados[2] = 0
                        n_clientes.append(estados[0])
                        t_clientes.append(round(float(t), 3))
                        t2 = np.inf
                        continue

                    case [n, *_] if n > 2:
                        m = max(estados[1], estados[2])
                        estados[0] -= 1
                        estados[2] = m + 1

                        A[f"Cliente {m+1}"] = round(float(t), 3)

                        n_clientes.append(estados[0])
                        t_clientes.append(round(float(t), 3))
                        t2 = t + np.random.exponential(lambda_s2)
                        if t2 > tmax:
                            restante += 1
                        S[f"Cliente {m+1}"] = 2
                        continue

        else:
            if t1 <= t2:
                t = t1
                P[f"Cliente {estados[1]}"] = round(float(t), 3)

                match estados:
                    case [1, *_]:
                        estados = [0, 0, 0]
                        n_clientes.append(estados[0])
                        t_clientes.append(round(float(t), 3))
                        t1 = np.inf
                        continue

                    case [2, *_]:
                        estados[0] = 1
                        estados[1] = 0
                        n_clientes.append(estados[0])
                        t_clientes.append(round(float(t), 3))
                        t1 = np.inf
                        continue

                    case [n, *_] if n > 2:
                        m = max(estados[1], estados[2])
                        estados[0] -= 1
                        estados[1] = m + 1

                        A[f"Cliente {m+1}"] = round(float(t))

                        n_clientes.append(estados[0])
                        t_clientes.append(round(float(t), 3))
                        t1 = t + np.random.exponential(lambda_s1)
                        if t1 > tmax:
                            restante += 1
                        S[f"Cliente {m + 1}"] = 1
                        continue
            else:
                t = t2
                P[f"Cliente {estados[2]}"] = round(float(t), 3)

                match estados:
                    case [1, *_]:
                        estados = [0, 0, 0]
                        n_clientes.append(estados[0])
                        t_clientes.append(round(float(t), 3))
                        t2 = np.inf
                        continue

                    case [2, *_]:
                        estados[0] = 1
                        estados[2] = 0
                        n_clientes.append(estados[0])
                        t_clientes.append(round(float(t), 3))
                        t2 = np.inf
                        continue

                    case [n, *_] if n > 2:
                        m = max(estados[1], estados[2])
                        estados[0] -= 1
                        estados[2] = m + 1

                        A[f"Cliente {m+1}"] = round(float(t), 3)

                        n_clientes.append(estados[0])
                        t_clientes.append(round(float(t), 3))
                        t2 = t + np.random.exponential(lambda_s2)
                        if t2 > tmax:
                            restante += 1
                        S[f"Cliente {m + 1}"] = 2
                        continue

    C = dict(sorted(C.items(), key=lambda item: int(item[0].split()[1])))
    P = dict(sorted(P.items(), key=lambda item: int(item[0].split()[1])))
    A = dict(sorted(A.items(), key=lambda item: int(item[0].split()[1])))
    S = dict(sorted(S.items(), key=lambda item: int(item[0].split()[1])))

    return n_clientes, t_clientes, restante, t, C, P, A, S


tmax = 480


#---------------------- Seção para obter dados médios, simulando múltiplas vezes --------------------------#
# tempo_pos = []
# medias_espera = []
# n_s1 = []
# n_s2 = []
#
# for i in range(5000):
#     n_clientes, t_clientes, _, t, C, _, A, S = simula_filaParalela(tmax, 1/5, 5, 5)
#     tempo_pos.append(t - tmax)
#     s1 = sum(1 for i in S.values() if i == 1)
#     n_s1.append(s1)
#     n_s2.append(len(S) - s1)
#     E = {cliente: round(float(A[cliente] - C[cliente]), 3) for cliente in A if cliente in C}
#     espera_media = sum(E.values())/len(E)
#     medias_espera.append(espera_media)
#
# print(f"Tempo médio de trabalho dos servidores pós fechamento: {max(np.mean(tempo_pos), 0):.2f}")
# print(f"Número Médio de Clientes do Servidor 1: {np.mean(n_s1)}")
# print(f"Número Médio de Clientes do Servidor 2: {np.mean(n_s2)}")
# print(f"Tempo Médio de Espera na Fila: {np.mean(medias_espera)}")
# ----------------------------------------------------------------------------------------------------------#


#-------------------------- Seção para uma única rodada e para gerar visualizações -------------------------#
n_clientes, t_clientes, _, _, _, _, _, _ = simula_filaParalela(480, 1/5, 5, 5)

# E = {chave: round(float(A[chave] - C[chave]), 3) for chave in A if chave in C}
#
# print(f"Tempo total: {t}")
# print(f"Número de clientes ainda na loja ao fechar: {restante}")
# print(f"Número de clientes em cada tempo de atualização: {n_clientes[:6]}\n")
# print(f"Tempos de Chegada: {dict(islice(C.items(), 5))}")
# print(f"Momentos de Atendimento: {dict(islice(A.items(), 5))}")
# print(f"Tempos de Partida: {dict(islice(P.items(), 5))}")
# print(f"Relação Cliente/Servidor: {dict(islice(S.items(), 5))}")

fig1 = go.Figure(data=go.Scatter(x=t_clientes, y=n_clientes, mode='markers+lines'))
fig1.update_layout(title="Número de Clientes no Sistema em Função do Tempo", xaxis_title="Tempo", yaxis_title="Clientes")
fig1.show()


#
# n_s1 = sum(1 for i in S.values() if i == 1)
# n_s2 = len(S) - n_s1
#
# fig2 = go.Figure(data=[go.Bar(x=['Servidor 1', 'Servidor 2'], y=[n_s1, n_s2], width = 0.3)])
# fig2.update_layout(title="Número Total de Clientes Atendidos por cada Servidor", yaxis_title="Clientes", yaxis = dict(range=[0, n_s1 + n_s2]))
# fig2.show()
#------------------------------------------------------------------------------------------------------------#









