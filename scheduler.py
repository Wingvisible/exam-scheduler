import pandas as pd
import itertools
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mpl
from networkx.utils import py_random_state

exams = pd.read_excel("exams.xlsx", sheet_name = 0, usecols = "A:C", header=None).fillna(0)
exams = exams.values
print(exams)

def get_node_edges(exams: np.array):
    exams_dictionary = {}
    exam_edges = []
    exam_student_count = {}
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
                exam_student_count[exam] = 0
            exam_student_count[exam] += 1
        for i in range(len(student)):
            for j in student[i+1:]:
                edge = [exams_dictionary[student[i]], exams_dictionary[j]]
                if tuple(edge) not in exam_edges and tuple(edge[::-1]) not in exam_edges:
                    exam_edges.append(tuple(edge))
    return exams_dictionary, exam_edges, exam_student_count

exams_dictionary, exam_edges, exam_student_count = get_node_edges(exams)

print(exams_dictionary)        
print(exam_edges)
print(f"exam count = {exam_student_count}")

G = nx.Graph()
G.add_edges_from(exam_edges)

#1. from networkx documentation https://networkx.org/documentation/stable/_modules/networkx/algorithms/coloring/greedy_coloring.html#greedy_color
@py_random_state(2)
def strategy_random_sequential(G, colors, seed=None):
    """Returns a random permutation of the nodes of ``G`` as a list.

    ``G`` is a NetworkX graph. ``colors`` is ignored.

    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.
    """
    nodes = list(G)
    seed.shuffle(nodes)
    return nodes

def strategy_largest_first(G, colors, seed):
    """Returns a list of the nodes of ``G`` in decreasing order by
    degree.

    ``G`` is a NetworkX graph. ``colors`` is ignored.

    """
    return sorted(G, key=G.degree, reverse=True)

def greedy_color(G, strategy, seed):
    colors = {}
    nodes = strategy(G, colors, seed)
    existing_colors = set()
    for u in nodes:
        # Set to keep track of colors of neighbors
        nbr_colors = {colors[v] for v in G[u] if v in colors}
        # Add slots that are in the same day. Day 1 has slot 0, 1 (only 1 morning and 1 afternoon slot every day)
        same_day_colors = []
        for colour in nbr_colors:
            if colour % 2 == 0:
                same_day_colors.append(colour+1)
            elif colour % 2 != 0:
                same_day_colors.append(colour-1)
        nbr_colors.update(same_day_colors)
        # Find the first unused color.
        Color = None
        for color in range(17):
            if color not in nbr_colors and color not in existing_colors:
                Color = color
                break
        if Color is None: 
            for color in itertools.count():
                if color not in nbr_colors:
                    break
        # Assign the new color to the current node.
        colors[u] = color
        existing_colors.update({color})
    return colors


# Run different node sequence orders
print(G.degree)
coloring = greedy_color(G, strategy=strategy_largest_first, seed=None)
best_coloring = coloring
print(set(coloring.values()))
least_slots = max(set(coloring.values()))
for seed in range(100):
    coloring = greedy_color(G, strategy=strategy_random_sequential, seed=seed)
    required_slots = max(set(coloring.values()))
    if required_slots < least_slots:
        best_coloring = coloring
        least_slots = required_slots


#2. from https://networkx.org/documentation/stable/auto_examples/algorithms/plot_greedy_coloring.html
unique_colors = set(best_coloring.values())
print(f"number of colors: {least_slots}, color map = {best_coloring}")
# Assign colors to nodes based on the greedy coloring
graph_color_to_mpl_color = dict(zip(unique_colors, mpl.CSS4_COLORS))
node_colors = [graph_color_to_mpl_color[best_coloring[n]] for n in G.nodes()]

#3. from https://networkx.org/documentation/stable/auto_examples/basic/plot_simple_graph.html
options = {
    "font_size": 10,
    "node_size": 500,
    "node_color": node_colors, #here I use the color mapping in 2.
    "edgecolors": "black",
    "linewidths": 1,
    "width": 2,
}

daily_student_count = []
for i in range(least_slots+1):
    if i % 2 == 0:
        count = 0
        for exam,color in best_coloring.items():
            if color == i or color == i+1:
                for k,v in exams_dictionary.items():
                    if v == exam:
                        count += exam_student_count[k]
        daily_student_count.append(count)
print(daily_student_count)    

nx.draw_networkx(G, **options)
plt.axis("off")
plt.show()