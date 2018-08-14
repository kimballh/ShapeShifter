from kallisto import kallistoToPandas
import os
import tempfile
import zipfile
import pandas as pd
import re

class KallistoFile(SSFile):

    def read_input_to_pandas(self, columnList=[], indexCol="Sample"):
        df = kallistoToPandas(self.filePath)
        #can I read in only certain columns? 
        if len(columnList) > 0:
            df = df[columnList]
        return df
