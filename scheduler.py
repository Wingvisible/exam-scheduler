import pandas as pd

exams = pd.read_excel("exams.xlsx", sheet_name = 0, usecols = "A:C", header=None)
print(exams.values)
