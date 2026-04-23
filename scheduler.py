import pandas as pd
import numpy as np

exams = pd.read_excel("exams.xlsx", sheet_name = 0, usecols = "A:C", header=None).fillna(0)
exams = exams.values[0:10]
print(exams)

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


print(exams_dictionary, exam_count)        
print(exam_edges)

