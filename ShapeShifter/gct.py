import pandas as pd

#Takes a pandas dataframe and converts it to a file
#The file will be named after the second parameter
def toGCT(df, fileName):
    df = df.fillna("") 
#Write #1.2 (the version string)
    writeFile = open(fileName, 'w')
    writeFile.write("#1.2\n")
#Write the number of rows and the number of columns
    writeFile.write(str(len(df.index))) 
    writeFile.write("\t" + str(len(df.columns[2:])) + "\n")
#Write the data
    writeFile.write(str(df)) 
    writeFile.close()	
