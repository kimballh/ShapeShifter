import pandas as pd

#Takes a pandas dataframe and converts it to a file
#The file will be named after the second parameter
def toGCT(df, fileName):
    #df = df.fillna("")
#Write #1.2 (the version string)
    writeFile = open(fileName, 'w')
    writeFile.write("#1.2\n")
#Write the number of rows and the number of columns
    writeFile.write(str(len(df.index)))
    writeFile.write("\t" + str(len(df.columns[1:])) + "\n")
    writeFile.close()
#Write the dataframe
    df.to_csv(path_or_buf=fileName, sep="\t", na_rep="", mode='a')
#Manually add a description column. Copy the values in Name over if there's a name column. If no NAME column, throw a descriptive error saying that we need one. 

#Takes a GCT file and reads it into a pandas dataframe
def gctToPandas(fileName):
#We're trying to keep it from having the default index
    df = pd.read_csv(filepath_or_buffer=fileName, sep='\t', index_col=False, skiprows=2)
#Also remove the description column.
    return df

#Make these changes and run it again. 
