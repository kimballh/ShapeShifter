import pandas as pd
def gctToPandas(fileName):
    df = pd.read_csv(filepath_or_buffer="allaml.dataset.gct", sep='\t', skiprows=2)
    return df
