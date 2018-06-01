import pandas as pd

def gctToPandas(fileName):
    col = []
    data = []
    with open(fileName) as readFile: 
        i = 0
        for line in readFile:
            line = line.rstrip("\n")
            i += 1
            if i <= 2:
                continue
            if i == 3:
                col = line.split("\t")
            else:
                data.append(line.split("\t"))
    df = pd.DataFrame(data, columns=col)
    return df 


