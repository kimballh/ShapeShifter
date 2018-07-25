import pandas as pd
import re
import numpy as np

#Converts an ARFF file (the parameter) into a pandas dataframe
def arffToPandas(fileName):
    i = 0
    columnNames = []
    dataList = []
    pattern = r"@[Aa][Tt][Tt][Rr][Ii][Bb][Uu][Tt][Ee]\s+([^\s]*)\s+.*"
    with open(fileName) as dataFile:
        for line in dataFile: 
            i += 1 
            line = line.rstrip("\n")
#Takes the column names in the attribute and put them in a list 
            if line.startswith("@ATTRIBUTE") or line.startswith("@attribute"):  
                columnNames.append(re.sub(pattern, r"\1", line)) 
                continue
            elif line.startswith("@DATA") or line.startswith("@data"):
                break
            elif line.startswith("@") or line.startswith("%") or line == "":
                continue
              
#Turns the lines into lists and put them into a list

    data = pd.read_csv(filepath_or_buffer=fileName, sep=',', names=columnNames, skiprows=i)

    data = data.replace("?", np.nan)

    return data 
   







