import networkx as nx
from networkx.drawing.nx_pydot import (write_dot, to_pydot)

import sys
import itertools
import random

if __name__ == '__main__':
    n = int(sys.argv[1])

    vs = list(itertools.combinations([str(x) for x in range(0, n)], 2))

    e = random.sample(vs, random.randint(n//2, (n*(n-1))//2))
    
    G = nx.Graph()
    G.add_edges_from(e)
    
    print(to_pydot(G).to_string())
