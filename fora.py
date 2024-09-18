import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import math

G = nx.karate_club_graph() #34 nodes in this network graph


def forward_push(G, s, alpha, r_max):
    pi = {node: 0 for node in G.nodes}
    r = {node: 0 for node in G.nodes}
    r[s] = 1

    while True:
        push_nodes = [v for v in G.nodes if r[v] / len(G[v]) > r_max]
        if not push_nodes:
            break
        arbitrary_node = random.choice(push_nodes)
        out_neighbors = list(G[arbitrary_node])
        for u in out_neighbors:
            r[u] += (1 - alpha) * r[arbitrary_node] / len(out_neighbors)
        pi[arbitrary_node] += alpha * r[arbitrary_node]
        r[arbitrary_node] = 0
        print(f"pi value is: {pi}. \n r value is: {r}")
    return pi, r

# kara_pi, kara_r = forward_push(G, 2, 0.2, 0.05)

"""
# A simple test example as decribed in "Unifying the Global and Local Approaches" by H.Wu, J.Gan, Z.Wei and R.Zhang
g_test = nx.DiGraph()
g_test.add_nodes_from([1, 2, 3, 4, 5])
g_test.add_edges_from([(1,2), (1,3),(2,1),(2,3),(2,4),(2,5),(3,2), (3,4), (4,1), (4,2), (4,3), (5,2), (5,3)])

pi, r = forward_push(g_test, 1, 0.2, 0.099)
"""
     

def fora(G, s, alpha, r_max, pf, epsilon, delta):

    pi, r = forward_push(G, s, alpha, r_max)
    r_sum = sum(r)
    omega_value = r_sum * (2 * epsilon / 3 + 2) * math.log(2 / pf) / (pow(epsilon, 2) * delta)
    pi_hat = pi
    omega = {node: 0 for node in G.nodes}
    a = {node: 0 for node in G.nodes}
    active_nodes = [v for v in G.nodes if r[v] > 0]
    for v in active_nodes:
        omega[v] = math.ceil(r[v] * omega_value / r_sum)
        a[v] = r[v] * omega_value / (r_sum * omega[v])
        for i in range(1, omega[v] + 1):
            # Random walk from v to t.
            t = random.choice(list(G[v]))
            pi_hat[t] += a[v] * r_sum / omega_value
        print("1 random walk completed.")
    return pi_hat

"""
pi_hat_test = fora(g_test, s = 2)
print(pi_hat_test)
# {1: 0.049971752217183765, 2: 0.6750264913912795, 3: 0.20002065557391127, 4: 0.07498110059412467, 5: 0}
"""

def top_k(G, s, alpha, k, pf, r_max, epsilon, delta):
    n_val = G.number_of_nodes()
    pf_new = pf / (n_val * math.log(n_val))
    for i in range(2, n_val + 1):
        delta = 1 / i
        pi_hat = fora(G, s, alpha, r_max, pf_new, epsilon, delta)
        sorted_nodes = sorted(pi_hat.items(), key=lambda x: x[1], reverse=True)
        top_k_nodes = sorted_nodes[:k]
        LB = {v: max(0, ppr - random.random() * 0.1) for v, ppr in pi_hat.items()}
        UB = {v: min(1, ppr + random.random() * 0.1) for v, ppr in pi_hat.items()}
        # The conditions parts are confusing. TBC
    return [(v, pi_hat[v]) for v, _ in top_k_nodes]

            

g_test = nx.DiGraph()
g_test.add_nodes_from([1, 2, 3, 4, 5])
g_test.add_edges_from([(1,2), (1,3),(2,1),(2,3),(2,4),(2,5),(3,2), (3,4), (4,1), (4,2), (4,3), (5,2), (5,3)])

s = 1
alpha = 0.2
k = 3
pf = 0.05
r_max = 0.09
epsilon = 0.01
delta = 1e-3

result = top_k(g_test, s, alpha, k, pf, r_max, epsilon, delta)
print(result)