import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

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
options = {
    "font_size": 10,
    "node_size": 500,
    "node_color": "white",
    "edgecolors": "black",
    "linewidths": 1,
    "width": 2,
}
nx.draw_networkx(G, **options)
ax = plt.gca()
ax.margins(0.20)
plt.axis("off")
plt.show()