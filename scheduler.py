import pandas as pd
import itertools
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mpl

exams = pd.read_excel("exams.xlsx", sheet_name = 0, usecols = "A:C", header=None).fillna(0)
exams = exams.values[:10]
print(exams)

def get_node_edges(exams: np.array):
    exams_dictionary = {}
    exam_edges = []

    exam_count = 0
    for student in exams:
        student = list(student)
        for value in student:
            if value == 0:
                student.remove(value)
        print(student)    
        for exam in student:
            if exam not in exams_dictionary:
                exams_dictionary[exam] = exam_count
                exam_count += 1
        for i in range(len(student)):
            for j in student[i+1:]:
                edge = [exams_dictionary[student[i]], exams_dictionary[j]]
                if tuple(edge) not in exam_edges and tuple(edge[::-1]) not in exam_edges:
                    exam_edges.append(tuple(edge))
    return exams_dictionary, exam_edges

exams_dictionary, exam_edges = get_node_edges(exams)

print(exams_dictionary)        
print(exam_edges)

G = nx.Graph()
G.add_edges_from(exam_edges)

#1. from networkx documentation https://networkx.org/documentation/stable/_modules/networkx/algorithms/coloring/greedy_coloring.html#greedy_color
def strategy_largest_first(G, colors):
    """Returns a list of the nodes of ``G`` in decreasing order by
    degree.

    ``G`` is a NetworkX graph. ``colors`` is ignored.

    """
    return sorted(G, key=G.degree, reverse=True)

def greedy_color(G, strategy):
    colors = {}
    nodes = strategy(G, colors)
    for u in nodes:
        # Set to keep track of colors of neighbors
        nbr_colors = {colors[v] for v in G[u] if v in colors}
        # Find the first unused color.
        for color in itertools.count():
            if color not in nbr_colors:
                break
        # Assign the new color to the current node.
        colors[u] = color
    return colors


coloring = greedy_color(G, strategy=strategy_largest_first)

#2. from https://networkx.org/documentation/stable/auto_examples/algorithms/plot_greedy_coloring.html
unique_colors = set(coloring.values())
# Assign colors to nodes based on the greedy coloring
graph_color_to_mpl_color = dict(zip(unique_colors, mpl.TABLEAU_COLORS))
node_colors = [graph_color_to_mpl_color[coloring[n]] for n in G.nodes()]

#3. from https://networkx.org/documentation/stable/auto_examples/basic/plot_simple_graph.html
options = {
    "font_size": 10,
    "node_size": 500,
    "node_color": node_colors, #here I use the color mapping in 2.
    "edgecolors": "black",
    "linewidths": 1,
    "width": 2,
}
nx.draw_networkx(G, **options)
plt.axis("off")
plt.show()