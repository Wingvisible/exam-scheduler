import pandas as pd

exams = pd.read_excel("exams.xlsx", sheet_name = 0, usecols = "A:C", header=None)
exams = exams.values[0:10]
print(exams)

exams_dictionary = {}
exam_count = 0
for student in exams:
    for exam in student:
        if exam not in exams_dictionary:
            exams_dictionary[exam] = exam_count
            exam_count += 1
print(exams_dictionary, exam_count)        
