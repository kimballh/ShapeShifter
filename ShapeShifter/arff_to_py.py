import pandas as pd
import re

#Converts an ARFF file (the parameter) into a pandas dataframe
def arffToPandas(fileName):
    columnNames = []
    dataList = []
    pattern = r"@[Aa][Tt][Tt][Rr][Ii][Bb][Uu][Tt][Ee]\s+([^\s]*)\s+.*"
    with open("diabetes.arff") as dataFile:
        for line in dataFile: 
            line = line.rstrip("\n")
#Takes the column names in the attribute and put them in a list 
            if line.startswith("@ATTRIBUTE") or line.startswith("@attribute"):  
                columnNames.append(re.sub(pattern, r"\1", line)) 
                continue
            elif line.startswith("@") or line.startswith("%") or line == "":
                continue
#Turns the lines into lists and put them into a list
            line = line.replace("?", "") 
            dataList.append(line.split(","))      
    data = pd.DataFrame(dataList, columns = columnNames)
    return data 
    







