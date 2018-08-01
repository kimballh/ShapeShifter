import pandas as pd

def read_input_to_pandas(self, columnList=[], indexCol="Sample"):
   
    #if the file is zipped, unzip it 
    if self.isGzipped:
        tempFile = super()._gunzip_to_temp_file()
        #read the unzipped tempfile into a dataframe
        df=pd.read_hdf(path_or_buf = tempFile.name)
        #delete the tempfile
        os.remove(tempFile.name)
    else:
        df = pd.read_hdf(path_or_buf = self.filePath)
        df = df.reset_index() 
    
    #initialize  
    begin = 0
    end = 0
    hitSample = False 

    #count on what line !Sample_ begins and how many lines are !Sample_ lines
    with open(self.filePath) as readFile:
        for line in readFile:
            #find the line on which !Sample_ starts
            if not line.startswith("!Sample_") and hitSample == False:
                begin += 1 
            #find how many lines start with !Sample_ 
            elif line.startswith("!Sample_"):
                hitSample = True
                end += 1 
            #stop looping through lines after !Sample_ lines 
            else:
                break

    #read the !Sample_ lines into a dataframe 
    df = pd.read_csv(filepath_or_buffer=self.filePath, sep="\t", header=None, index_col=0, skiprows=range(0, begin), nrows=end-1)
    #transpose the dataframe
    df = df.T
    #remove the !Sample_ prefix from the column names
    df.columns = df.columns.str[8:]
    #rename the "geo_accession" to "Sample"
    df = df.rename(columns={"geo_accession": "Sample"})
    #set the values in the "Sample" column to the row names
    df = df.set_index("Sample")
    #reduce the dataframe to only the requested columns
    if len(columnList > 0):
        df = df[columnList]
    return df

   
          
          

        







