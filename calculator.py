import pandas as pd
import tabula
import re

# Choose PDF file with your expedient
file_path = "M:/Universidad/GRADO/expediente.pdf"

# Extracts the float if possible
def convert_float(x):
    if isinstance(x, float) == False:
        if re.findall(r"[-+]?\d*\.\d+|\d+", x).__len__() != 0:
            x = float('.'.join(re.findall(r"[-+]?\d*\.\d+|\d+", x)))
    return x
# Auxiliar function to filter strings from dataframe
def sin_nota(x):
    if isinstance(x, str):
        return None
    else:
        return x

def to_gpa(mark):
    # Convert scale 0-10 to 0-4
    if mark >= 9:
        return 4
    elif mark <= 9 and mark >= 7:
        return 3
    elif mark <= 7 and mark >= 5:
        return 2
    elif mark < 5:
        return 1

# Preparing the data
df = tabula.read_pdf(file_path, pages='all')
df = pd.concat(df)
df = pd.DataFrame({'credits': df['Créditos'], 'mark' : df['Calificación']})
# Drop nulls
df = df.dropna()
# Convert to numeric values
df.credits = df.credits.apply(convert_float)
df.mark = df.mark.apply(convert_float)
# Total number of credit coursed
creditos_totales = df.credits.values.sum()
# Delete credits without mark
df = df[df.mark == (df.mark.apply(sin_nota))]
# GPA implementation
df['gpa'] = df.mark.apply(to_gpa)

# Final calculation
gpa_final = (df.gpa * df.credits).sum() / df.credits.values.sum()
media_final = (df.mark * df.credits).sum() / df.credits.values.sum()
# Credits with Mark
marked_credits = df.credits.values.sum()

#Final display of results
print('You coursed %s credits, %s of them have a mark'%(creditos_totales, marked_credits))
print('Your Final ponderated GPA is : %s'%gpa_final)
print('Your Mean is %s'%media_final)
