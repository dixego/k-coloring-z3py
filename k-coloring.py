import networkx as nx
from networkx.drawing.nx_pydot import (write_dot, read_dot, to_pydot)

from seaborn import color_palette

from z3 import *

from pprint import pprint
from itertools import combinations, chain
import sys
import argparse

def _gen_vars(G, k):
    """ Regresa un diccionario con todas las variables v_c tal que v es un 
        vértice de la gráfica y c es uno de k colores indexado por vértices """
    return {n : [Bool(f'{n}_{c}') for c in range(k)] for n in G.nodes}

def _each_v_has_c(_vars):
    """ Para cada vértice genera la fórmula 'El vértice tiene algún color' """
    return [Or(_vars[v]) for v in _vars.keys()]


def _each_v_only_one_c(_vars):
    """ Para cada vértice genera la fórmula 'El vértice tiene sólo un color' """
    return [Not(And(comb[0], comb[1])) for _, v in _vars.items() for comb in
            combinations(v, 2)]

def _adj_not_same_c(G, _vars):
    """ Para cada pareja de vértices que comparta una arista, genera la fórmula
        'los vértices tienen colores distintos' """
    return [Not(And(zi[0], zi[1])) 
        for e in G.edges for zi in zip(_vars[e[0]], _vars[e[1]])]

def main(input_file, k, output_file=None):

    G = read_dot(input_file)

    dic = _gen_vars(G, k)

    f1 = _each_v_has_c(dic)

    f2 = _each_v_only_one_c(dic)

    f3 = _adj_not_same_c(G, dic)

    solver = Solver()
    solver.add(f1 + f2 + f3)

    if solver.check().r > 0:

        m = solver.model()
        colors = [p for p in chain(*dic.values()) if m[p]]

        palette = color_palette('pastel', k).as_hex()

        for c in colors:
            s = str(c)
            cc = s.split('_')
            G.nodes[cc[0]]['fillcolor'] = palette[int(cc[1])]
            G.nodes[cc[0]]['style'] = 'filled'
    
        if output_file:
            write_dot(G, output_file)
        else:
            print(to_pydot(G).to_string())

    else:
        print(f"No se pudo encontrar una {k}-coloración para la gráfica", file=sys.stderr)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Buscar k-coloraciones de gráficas')

    parser.add_argument(
        'input_file', 
        metavar='FILE', 
        type=str, 
        help='archivo fuente de la gráfica')

    parser.add_argument(
        '-k', '--k',
        type=int,
        required=True)

    parser.add_argument(
        '-o', '--output_file',
        type=str,
        required=False, default=None)

    parser.add_argument

    args = parser.parse_args()

    main(args.input_file, args.k, args.output_file)
