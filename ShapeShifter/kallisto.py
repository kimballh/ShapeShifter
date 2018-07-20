def kallistoToPandas(fileName): 
    df = pd.DataFrame() 
    i = 0 
    z = zipfile.ZipFile(fileName)
    #extract the zipfile and put the contents in a temp directory
    with tempfile.TemporaryDirectory() as temp: 
        z.extractall(temp)
        #parse through the directory
        for dirpath, dirs, files in sorted(os.walk(temp)):  
            for d in dirs:
                abundanceFilePath = os.path.join(d, "abundance.tsv") 

                if not os.path.exists(abundanceFilePath):
                    continue         
                #read the first file's contents into a dataframe 
                if i == 0: 
                    df = pd.read_csv(filepath_or_buffer=abundanceFilePath, sep="\t", index_col=0, usecols=["target_id", "tpm"]) 
                    df = df.rename(columns={"tpm": d})  
                #join other files onto the first dataframe 
                else:
                    tempdf = pd.read_csv(filepath_or_buffer=abundanceFilePath, sep = "\t", index_col=0, usecols=["target_id", "tpm"]) 
                    tempdf = tempdf.rename(columns={"tpm": d})
                    df = df.join(tempdf, how='inner') 
                i += 1
    # Make sure we found at least one file and throw an exception if we didn't.
    if d.empty:
        raise Exception("No abundance.tsv files were found.")

    #transpose the dataframe
    df = df.T 
    #rename the dataframe to "Sample"
    df.index = df.index.rename("Sample")
    df.columns.name = None  

    return df
