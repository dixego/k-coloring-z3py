from z3 import *
from networkx.drawing.nx_pydot import (read_dot, write_dot, to_pydot)

from seaborn import color_palette

import sys
import random


def main(G, k):

    # generamos k colores aleatorios
    colors = color_palette('pastel', k).as_hex()

    x = Int('x')
    y = Int('y')

    # función de coloración
    color = Function('color', IntSort(), IntSort())
    # predicado que determina si dos vértices son vecinos
    edge = Function('edge', IntSort(), IntSort(), BoolSort())


    # \All x y, edge(x,y) => edge(y,x)
    # (edge es simétrica)
    edge_sym = ForAll([x, y], Implies(edge(x, y), edge(y, x)))

    # \All x, color(x) >= 0 /\ color(x) < k
    # (el color de un vértice es 0 <= c <= k
    color_between_0_k = ForAll(x, And(color(x) >= 0, color(x) < k))

    # \All x y, edge(x, y) => color(x) != color(y)
    # (si dos vértices son adyacentes, sus colores son distintos)
    adj_colors_neq = ForAll([x, y], Implies(edge(x, y), color(x) != color(y)))

    s = Solver()

    s.add(edge_sym)
    s.add(color_between_0_k)
    s.add(adj_colors_neq)


    _vars = {}

    for e in G.edges:
        v = e[0]
        w = e[1]
        if _vars.get(v) is None:
            _vars[v] = Int(v)
        if _vars.get(w) is None:
            _vars[w] = Int(w)

        # agregamos todas las aristas entre vértices
        s.add(edge(Int(e[0]), Int(e[1])))

    if s.check().r > 0:
        m = s.model()

        for k, v in _vars.items():
            k_color = m.evaluate(color(v))
            k_color = int(k_color.as_long())
            G.nodes[k]['color'] = colors[k_color]
            G.nodes[k]['fillcolor'] = colors[k_color]
            G.nodes[k]['style'] = 'filled'


        print(to_pydot(G).to_string())

    else:
        print("unsat", file=sys.stderr)

if __name__ == '__main__':

    G = read_dot(sys.argv[1])
    k = int(sys.argv[2])
    main(G, k)
