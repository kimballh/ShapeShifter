import pandas as pd
import re
import numpy as np

#Converts an ARFF file (the parameter) into a pandas dataframe
def arffToPandas(fileName):
    columnNames = []
    dataList = []
    pattern = r"@[Aa][Tt][Tt][Rr][Ii][Bb][Uu][Tt][Ee]\s+([^\s]*)\s+.*"
   
  
    with open(fileName) as dataFile:
        for line in dataFile: 
            line = line.rstrip("\n")
#Takes the column names in the attribute and put them in a list 
            if line.startswith("@ATTRIBUTE") or line.startswith("@attribute"):  
                columnNames.append(re.sub(pattern, r"\1", line)) 
                continue
            elif line.startswith("@") or line.startswith("%") or line == "":
                continue
#Turns the lines into lists and put them into a list 
            dataList.append(line.split(","))      
    data = pd.DataFrame(dataList, columns = columnNames)
    data = data.replace("?", np.nan)
    for column in data:
#Finds columns with numbers and changes the datatype to int or float
        data[column] = pd.to_numeric(data[column], errors='ignore')
#Converts true/false strings into booleans
        for cell in data[column]:
            if str(cell).lower() == "true":
                data[column] = data[column].replace(cell, True)
            elif str(cell).lower() == "false":
                data[column] = data[column].replace(cell, False)
    return data 
    






