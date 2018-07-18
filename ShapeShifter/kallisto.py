def kallistoToPandas(fileName): 
    d = pd.DataFrame()
    filePattern = r".*\/([^\/]*)"
    newIndex = {}

    i = 0 
    z = zipfile.ZipFile(fileName)
    #extract the zipfile and put the contents in a temp directory
    with tempfile.TemporaryDirectory() as temp: 
        z.extractall(temp)
        #parse through the directory
        for dirpath, dirs, files in sorted(os.walk(temp)):  
            for filename in files:
                #read abundance.tsv file 
                if filename == "abundance.tsv":
                    fname = os.path.join(dirpath, "abundance.tsv") 
                    #collect directory names to use them for the index 
                    newIndex[len(newIndex)] = re.sub(filePattern, r"\1", dirpath) 
                    #read the first file's contents into a dataframe 
                    if i == 0: 
                        d = pd.read_csv(filepath_or_buffer=fname, sep="\t", index_col=0, usecols=["target_id", "tpm"]) 
                        d = d.rename(columns={"tpm": 0})  
                    #join other files onto the first dataframe 
                    else:
                        tempdf = pd.read_csv(filepath_or_buffer=fname, sep = "\t", index_col=0, usecols=["target_id", "tpm"]) 
                        tempdf = tempdf.rename(columns={"tpm": i})
                        d = d.join(tempdf, how='inner') 
                    i += 1
    #transpose the dataframe
    d = d.T
    #read in dictionary of indexes and directories 
    d = d.rename(index=newIndex)
    #rename the dataframe to "Sample"
    d.index = d.index.rename("Sample")
    d.columns.name = None  
    return d
