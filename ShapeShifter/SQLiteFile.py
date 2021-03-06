import tempfile

import pandas as pd

from SSFile import SSFile


class SQLiteFile(SSFile):

    def read_input_to_pandas(self, columnList=[], indexCol="Sample"):
        from sqlalchemy import create_engine
        filePath=self.filePath
        if self.isGzipped:
            tempFile = super()._gunzip_to_temp_file()
            engine = create_engine('sqlite:///'+tempFile.name)
            #filePath= tempFile.name
        else:
            engine = create_engine('sqlite:///' + filePath)
        table = filePath.split('.')[0]
        tableList = table.split('/')
        table = tableList[len(tableList) - 1]
        query = "SELECT * FROM " + table
        if len(columnList) > 0:
            query = "SELECT " + ", ".join(columnList) + " FROM " + table

        df = pd.read_sql(query, engine)
        # if self.isGzipped:
        #     os.remove(filePath)
        return df

    def export_filter_results(self, inputSSFile, column_list=[], query=None, transpose=False, include_all_columns=False,
                              gzip_results=False, index_col="Sample"):

        filePath=self.filePath #needs to be stored separately as a string, can't be turned to a file object
        if query != None:
            query = super()._translate_null_query(query)
        if inputSSFile.isGzipped:
            inputSSFile.filePath=gzip.open(inputSSFile.filePath)
        df = inputSSFile._filter_data(columnList=column_list, query=query,
                                      includeAllColumns=include_all_columns, indexCol=index_col)
        null = 'NA'
        includeIndex = False
        if len(df.columns) > 999:
            raise SizeExceededError.SizeExceededError("SQLite supports a maximum of 999 columns. Your data has " + str(
                len(df.columns)) + " columns. Please use a smaller data set or consider using a different file type")
            # print("Warning: SQLite supports a maximum of 999 columns. Your data has " + str(
            #     len(df.columns)) + " columns. Extra data has been truncated.")
            # df=df.iloc[:,0:999]
        chunksize = 999//len(df.columns)
        from sqlalchemy import create_engine

        if gzip_results:
            tempFile = tempfile.NamedTemporaryFile(delete=False)
            engine = create_engine('sqlite:///' + tempFile.name)
            table = filePath.split('.')[0]
            tableList = table.split('/')
            table = tableList[len(tableList) - 1]
            if not transpose:
                df = df.set_index(index_col) if index_col in df.columns else df.set_index(df.columns[0])

                df.to_sql(table, engine, index=True, if_exists="replace", chunksize=chunksize)
            else:
                index_col = df.columns[0]
                df = df.set_index(index_col) if index_col in df.columns else df.set_index(df.columns[0])

                df = df.transpose()
                df.to_sql(table, engine, if_exists="replace", index=True, index_label=index_col, chunksize=chunksize)
            tempFile.close()
            super()._gzip_results(tempFile.name, filePath)

        else:
            engine = create_engine('sqlite:///' + super()._remove_gz(filePath))
            table = filePath.split('.')[0]
            tableList = table.split('/')
            table = tableList[len(tableList) - 1]
            if not transpose:
                df = df.set_index(index_col) if index_col in df.columns else df.set_index(df.columns[0])
                df.to_sql(table, engine, if_exists='replace', chunksize=chunksize)
            else:
                index_col = df.columns[0]
                df = df.set_index(index_col) if index_col in df.columns else df.set_index(df.columns[0])
                df = df.transpose()
                df.to_sql(table, engine, if_exists="replace", index=True, index_label=index_col, chunksize=chunksize)

    def write_to_file(self, df, gzipResults=False, includeIndex=False, null='NA', indexCol="Sample", transpose=False):
        filePath = self.filePath
        if len(df.columns) > 999:
            raise SizeExceededError.SizeExceededError("SQLite supports a maximum of 999 columns. Your data has " + str(
                len(df.columns)) + " columns. Please use a smaller data set or consider using a different file type")
        from sqlalchemy import create_engine
        chunksize = 999 // len(df.columns)
        # if gzipResults:
        #     tempFile= tempfile.NamedTemporaryFile(delete=False)
        #     engine = create_engine('sqlite:///' + tempFile.name)
        #     table = filePath.split('.')[0]
        #     tableList = table.split('/')
        #     table = tableList[len(tableList) - 1]
        #     df.to_sql(table,engine, index=True, if_exists="replace", chunksize=chunksize)
        #     tempFile.close()
        #     super()._gzip_results(tempFile.name, filePath)
        # else:
        #     engine = create_engine('sqlite:///' + super()._remove_gz(filePath))
        #     table = filePath.split('.')[0]
        #     tableList = table.split('/')
        #     table = tableList[len(tableList) - 1]
        #     df.to_sql(table, engine, index=True, if_exists="replace", chunksize=chunksize)
        if gzipResults:
            tempFile = tempfile.NamedTemporaryFile(delete=False)
            engine = create_engine('sqlite:///' + tempFile.name)
            table = filePath.split('.')[0]
            tableList = table.split('/')
            table = tableList[len(tableList) - 1]
            if not transpose:
                df = df.set_index(indexCol) if indexCol in df.columns else df.set_index(df.columns[0])

                df.to_sql(table, engine, index=True, if_exists="replace", chunksize=chunksize)
            else:
                indexCol = df.columns[0]
                df = df.set_index(indexCol) if indexCol in df.columns else df.set_index(df.columns[0])
                df = df.transpose()
                df.to_sql(table, engine, if_exists="replace", index=True, index_label=indexCol, chunksize=chunksize)
            tempFile.close()
            super()._gzip_results(tempFile.name, filePath)

        else:
            engine = create_engine('sqlite:///' + super()._remove_gz(filePath))
            table = filePath.split('.')[0]
            tableList = table.split('/')
            table = tableList[len(tableList) - 1]
            if not transpose:
                df = df.set_index(indexCol) if indexCol in df.columns else df.set_index(df.columns[0])
                df.to_sql(table, engine, if_exists='replace', chunksize=chunksize)
            else:
                indexCol = df.columns[0]
                df = df.set_index(indexCol) if indexCol in df.columns else df.set_index(df.columns[0])
                df = df.transpose()
                df.to_sql(table, engine, if_exists="replace", index=True, index_label=indexCol, chunksize=chunksize)

import gzip
import SizeExceededError