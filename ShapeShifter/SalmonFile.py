from salmon import salmonToPandas
import os
import tempfile
import zipfile
import pandas as pd

class SalmonFile(SSFile):

    def read_input_to_pandas(self, columnList=[], indexCol="Sample"):
        df = salmonToPandas(self.filePath)
        #can I read in only certain columns? 
        if len(columnList) > 0:
            df = df[columnList]
        return df
