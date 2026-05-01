import pandas as pd
import itertools
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mpl
from networkx.utils import py_random_state



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
                exam_student_count[exam_count] = 0
                exam_count += 1
            exam_student_count[exams_dictionary[exam]] += 1
        for i in range(len(student)):
            for j in student[i+1:]:
                edge = [exams_dictionary[student[i]], exams_dictionary[j]]
                if tuple(edge) not in exam_edges and tuple(edge[::-1]) not in exam_edges:
                    exam_edges.append(tuple(edge))
    return exams_dictionary, exam_edges, exam_student_count

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
    two_exams_same_day_count = 0
    colors = {}
    for u in nodes:
        # Set to keep track of colors of neighbors
        nbr_colors = {colors[v] for v in G[u] if v in colors}

        # # requirement 9 days but students can have 2 exams same day
        # # Find the first unused color.
        # for color in itertools.count():
        #     if color not in nbr_colors:
        #         break
        # #Assign the new color to the current node.
        # colors[u] = color


        # requirement no students have 2 exams the same day
        # Add slots that are in the same day. Day 1 has slot 0, 1 (only 1 morning and 1 afternoon slot every day)
        same_day_colors = []
        for colour in nbr_colors:
            if colour % 2 == 0 and color + 1 not in nbr_colors:
                same_day_colors.append(colour+1)
            elif colour % 2 != 0 and color - 1 not in nbr_colors:
                same_day_colors.append(colour-1)
        #print(nbr_colors)
        #print(f"same day colors: {same_day_colors}")
        nbr_colors.update(same_day_colors)
        #print(nbr_colors)
        #Find the first unused color.
        Color = None
        for color in range(18):
            if color not in nbr_colors and color not in existing_colors:
                Color = color
                break
        if Color is None: 
            for color in range(18):
                if color not in nbr_colors:
                    Color = color
                    break
            if Color is None:
                #print(f"basic: {nbr_colors}")
                nbr_colors.difference(same_day_colors)
                #print(f"basic: {nbr_colors}")
                for color in itertools.count():
                    if color not in nbr_colors:
                        print(u)
                        print(f"exam {exam_student_count[u]}")
                        two_exams_same_day_count += exam_student_count[u]
                        break
        #Assign the new color to the current node.
        colors[u] = color
        existing_colors.update({color})
    print(f"two exam on same day count = {two_exams_same_day_count}")
    return colors, two_exams_same_day_count

def daily_student_count(slots_number, coloring):
    daily_student_count = []
    for i in range(slots_number):
        if i % 2 == 0:
            count = 0
            for exam, slot in coloring.items():
                if slot == i or slot == i+1:
                    count += exam_student_count[exam]
            daily_student_count.append(count)
    return daily_student_count    

def celine_schedule_analysis(coloring, exams, daily_exam):
    conflict_count = 0
    for student in exams:
        #remove 0 at the end of the list
        student = list(student)
        for value in student:
            if value == 0:
                student.remove(value)
        conflict_found = False
        student_exam_numbers = [coloring[exams_dictionary[exam]] for exam in student]
        if len(set(student_exam_numbers)) < len(student_exam_numbers):
            conflict_count += 1
    print(conflict_count)
exams = pd.read_excel("exams.xlsx", sheet_name = 0, usecols = "A:C", header=None).fillna(0)
exams = exams.values
print(exams)

exams_dictionary, exam_edges, exam_student_count = get_node_edges(exams)

print(exams_dictionary)        
print(exam_edges)
print(f"exam count = {exam_student_count}")

G = nx.Graph()
G.add_edges_from(exam_edges)


# Run different node sequence orders
print(G.degree)
coloring, two_exam_same_day_count = greedy_color(G, strategy=strategy_largest_first, seed=None)
best_coloring = coloring
print(set(coloring.values()))
least_slots = max(set(coloring.values()))+1
max_daily_student_count = max(daily_student_count(least_slots, coloring))
max_two_exam_same_day_count = two_exam_same_day_count
for seed in range(100):
    coloring, two_exam_same_day_count = greedy_color(G, strategy=strategy_random_sequential, seed=seed)
    required_slots = max(set(coloring.values())) + 1
    if required_slots <= least_slots:
        max_student_count = max(daily_student_count(required_slots, coloring))
        print("hi", max_student_count)
        if max_student_count <= max_daily_student_count and two_exam_same_day_count <= max_two_exam_same_day_count:
            best_coloring = coloring
            least_slots = required_slots
            max_daily_student_count = max_student_count


#2. from https://networkx.org/documentation/stable/auto_examples/algorithms/plot_greedy_coloring.html
unique_colors = set(best_coloring.values())
print(f"number of colors: {least_slots}, color map = {best_coloring}, max students in a day = {max_daily_student_count}, students taking two exams same day = {max_two_exam_same_day_count}")
print(f"daily student count: {daily_student_count(least_slots, best_coloring)}" )
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

celine_coloring = {0:2, 14:2, 5:0, 17:0, 10:1, 20:4, 11:4, 6:6, 16:7, 19:7, 21:8, 3:8, 7:8, 1:10, 13:12, 9:12, 18:12, 12:14, 4:15, 15:15, 2:16, 22:16, 8:16 }
daily_celine_exams = [(5,17,10), (14,0), (20,11), (6,16,19), (21,3,7), (1), (13,9,18), (12,4,15), (2,22,8)]
celine_coloring_only_morning = {5:0, 17:0, 10:0, 14:1, 0:1, 20:2, 11:2, 6:3, 16:3, 19:3, 21:4, 3:4, 7:4, 1:5, 13:6, 9:6, 18:6, 12:7, 4:7, 15:7, 2:8, 22:8, 8:8}
celine_schedule_analysis(celine_coloring_only_morning, exams, daily_celine_exams)

nx.draw_networkx(G, **options)
plt.axis("off")
plt.show()