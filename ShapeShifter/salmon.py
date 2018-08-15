import pandas as pd
import zipfile
import os
import tempfile

def salmonToPandas(fileName): 
    df = pd.DataFrame() 
    i = 0 
    z = zipfile.ZipFile(fileName)
    #extract the zipfile and put the contents in a temp directory
    with tempfile.TemporaryDirectory() as temp: 
        z.extractall(temp)
        #parse through the directory
        for dirpath, dirs, files in sorted(os.walk(temp)):  
            for d in dirs:
                abundanceFilePath = os.path.join(d, "quant.sf") 

                if not os.path.exists(abundanceFilePath):
                    continue         
                #read the first file's contents into a dataframe 
                if i == 0: 
                    df = pd.read_csv(filepath_or_buffer=abundanceFilePath, sep="\t", index_col=0, usecols=["Name", "TPM"]) 
                    df = df.rename(columns={"TPM": d}) 
                #join other files onto the first dataframe 
                else:
                    tempdf = pd.read_csv(filepath_or_buffer=abundanceFilePath, sep = "\t", index_col=0, usecols=["Name", "TPM"]) 
                    tempdf = tempdf.rename(columns={"TPM": d})
                    df = df.join(tempdf, how='inner') 
                i += 1
    # Make sure we found at least one file and throw an exception if we didn't.
    if df.empty:
        raise Exception("No abundance.tsv files were found in {}.".format(fileName))

    #transpose the dataframe
    df = df.T 
    #rename the dataframe to "Sample"
    df.index = df.index.rename("Sample")
    df.columns.name = None  

    return df
#Two different parsers for Salmon; two for kallisto.
#Kallisto_tpm and kallisto_est_counts
#Salmon_tpm and salmon_numreads
#Make capitalization consistent with that in the file (TPM)
#Change "abundance" to "quant."  
#Add argument to function to specify column names? TPM or NumReads
