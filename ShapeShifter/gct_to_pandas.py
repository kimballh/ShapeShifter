import pandas as pd

#Takes a GCT file and reads it into a pandas dataframe
def gctToPandas(fileName):
    col = []
    data = []
    with open(fileName) as readFile: 
        i = 0
        for line in readFile:
            line = line.rstrip("\n")
            i += 1
#Skip the first two lines
            if i <= 2:
                continue
#Read the column names into a list
            if i == 3:
                col = line.split("\t")
#Read the rest of the data into a list of lists
            else:
                data.append(line.split("\t"))
    df = pd.DataFrame(data, columns=col)
    return df 


