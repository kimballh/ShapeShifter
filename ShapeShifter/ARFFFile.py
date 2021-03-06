import os
import tempfile

from ConvertARFF import arffToPandas
from ConvertARFF import toARFF
from SSFile import SSFile


class ARFFFile(SSFile):

    def read_input_to_pandas(self, columnList=[], indexCol="Sample"):
        if self.isGzipped:
            tempFile = super()._gunzip_to_temp_file()
            df= arffToPandas(tempFile.name)
            os.remove(tempFile.name)
        else:
            df = arffToPandas(self.filePath)
        if len(columnList) > 0:
            df = df[columnList]
        return df

    def export_filter_results(self, inputSSFile, column_list=[], query=None, transpose=False, include_all_columns=False,
                              gzip_results=False, index_col="Sample"):
        df = None
        includeIndex = False
        null = 'NA'
        query, inputSSFile, df, includeIndex = super()._prep_for_export(inputSSFile, column_list, query, transpose,
                                                                        include_all_columns, df, includeIndex, index_col)

        self.write_to_file(df, gzip_results, includeIndex, null)

    def write_to_file(self, df, gzipResults=False, includeIndex=False, null='NA', indexCol="Sample", transpose=False):
        if gzipResults:
            tempFile = tempfile.NamedTemporaryFile(delete=False)
            toARFF(df, tempFile.name)
            tempFile.close()
            super()._gzip_results(tempFile.name, self.filePath)
        else:
            toARFF(df, super()._remove_gz(self.filePath))





