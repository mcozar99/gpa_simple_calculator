import pandas as pd
import tabula
import numpy as np
import re
import math

# Choose PDF file with your expedient
file_path = "M:/Universidad/GRADO/expediente.pdf"

# Preparing the data
df = tabula.read_pdf(file_path, pages='all')

credit_list = []
grade_list = []
for page in df:
    credit_list.append(page['Créditos'].values)
    grade_list.append(page['Calificación'].values)
credit_list = list(np.concatenate(credit_list, axis=0))
grade_list = list(np.concatenate(grade_list, axis=0))

i = 0
while i < (grade_list.__len__()):
    if isinstance(grade_list[i], float) == False and grade_list[i] is not None:
        if re.findall(r"[-+]?\d*\.\d+|\d+", grade_list[i]).__len__() != 0:
            grade_list[i] = float('.'.join(re.findall(r"[-+]?\d*\.\d+|\d+", grade_list[i])))
    if isinstance(credit_list[i], float) == False and credit_list[i] is not None:
        if re.findall(r"[-+]?\d*\.\d+|\d+", credit_list[i]).__len__() != 0:
            credit_list[i] = float('.'.join(re.findall(r"[-+]?\d*\.\d+|\d+", credit_list[i])))
    i+=1

for mark in grade_list:
    if isinstance(mark, float) == False:
        credit_list.pop(grade_list.index(mark))
        grade_list.remove(mark)

grade_list = [x for x in grade_list if pd.isnull(x) == False and x != 'nan']
credit_list = [x for x in credit_list if pd.isnull(x) == False and x != 'nan']


# Convert scale 0-10 to 0-4
gpa_list = []
for mark in grade_list:
    if mark >= 9:
        gpa_list.append(4)
    elif mark <= 9 and mark >= 7:
        gpa_list.append(3)
    elif mark <= 7 and mark >= 5:
        gpa_list.append(2)
    elif mark < 5:
        gpa_list.append(1)


#Calculation of accumulative gpa and mean
creditos_totales = sum(credit_list)
media_acumulada = 0
gpa_acumulado = 0
i = 0
while i < gpa_list.__len__():
    gpa_acumulado += gpa_list[i]*credit_list[i]
    media_acumulada += grade_list[i]*credit_list[i]
    i+=1

#Final calculation of parameters
media_final = media_acumulada/creditos_totales
gpa_final = gpa_acumulado/creditos_totales
absolute_gpa = sum(gpa_list)/len(gpa_list)
absolute_mean = sum(grade_list)/len(grade_list)



#Final display of results
print('Your Final ponderated GPA is : %s'%gpa_final)
print('Your absolute GPA is %s'%absolute_gpa)
print('Your Mean is %s'%media_final)
print('Your absolute Mean is %s'%absolute_mean)