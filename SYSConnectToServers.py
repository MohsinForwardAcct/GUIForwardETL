from sqlalchemy.engine import URL
from sqlalchemy import create_engine
import pandas as pd
import pyodbc
import os
from dotenv import load_dotenv
load_dotenv()

# handle ODS server connections, fetch and append data queries 
    
class ConnectToODSServer():

    def __init__(self):

        self.ODSServer = os.getenv("ODSServer")
        self.ODSDatabase = os.getenv("ODSDatabase")
        self.ODSUser = os.getenv("ODSUser")
        self.ODSPassword = os.getenv("ODSPassword")
        Driver ='ODBC Driver 17 for SQL Server'
        self.ODSConnectionString = f'Driver={Driver};Server={self.ODSServer};Database={self.ODSDatabase};UID={self.ODSUser};PWD={self.ODSPassword}'
        self.ODSConnection = URL.create("mssql+pyodbc", query={"odbc_connect": self.ODSConnectionString})
        self.engineODS = create_engine(self.ODSConnection, use_setinputsizes = False, echo = False)
        self.ODSConnectionPandas = self.engineODS.connect()
        self.ODSConnection = pyodbc.connect(self.ODSConnectionString)

    # try and append data to ODS server 

    def qryODSAppendData(self, query):
        try: return self.ODSConnection.execute(query).commit()
        except Exception as e: print(f"error message {e}"); pass

    # try and extract data from ODS server 
    
    def qryODSGetData(self, query):
        try: return pd.read_sql(query, con=self.ODSConnectionPandas)
        except Exception as e: print(f"error message {e}"); pass
    
# handle ETL server connections, fetch and append data queries 
    
class ConnectToETLServer():

    def __init__(self):

        Driver ='ODBC Driver 17 for SQL Server'
        self.ETLServer = os.getenv("ETLServer")
        self.ETLDatabase = os.getenv("ETLDatabase")
        self.ETLUser = os.getenv("ETLUser")
        self.ETLPassword = os.getenv("ETLPassword")
        self.ETLConnectionString = f'Driver={Driver};Server={self.ETLServer};Database={self.ETLDatabase};UID={self.ETLUser};PWD={self.ETLPassword}'
        self.ETLConnection = URL.create("mssql+pyodbc", query={"odbc_connect": self.ETLConnectionString})
        self.engineETL = create_engine(self.ETLConnection, use_setinputsizes = False, echo = False)
        self.ETLConnectionPandas = self.engineETL.connect()
        self.ETLConnection = pyodbc.connect(self.ETLConnectionString)

    # try and append data to ETL server 

    def qryETLAppendData(self, query):
        try: return self.ETLConnection.execute(query).commit()
        except Exception as e: print(f"error message {e}"); pass

    # try and extract data from ETL server 
    
    def qryETLGetData(self, query):
        try: return pd.read_sql(query, con=self.ETLConnectionPandas)
        except Exception as e: print(f"error message {e}"); pass
    
# handle ODS server connections, load data queries 
    
class LoadDataToODS():

    def LoadDataToODS(self, Data, TableName):

        DateList  = ['DATE','SaleDate','QuoteDate','CreatedOn','TransactionDate','TimeStamp','AccountEffectiveDate','InvoiceDate']
        ErrList = ['nan', 'None', 'NaT']
        for index, Lines in Data.iterrows():
            qrySelect = ''; qryInsert = ''
            for ColumnName in Lines.index: 
                RowData =  Lines[ColumnName]; qryInsert = qryInsert+'['+ColumnName+'], '  
                RowData = str(RowData).replace("'","")   
                if RowData in ErrList: RowData = ''
                if ColumnName in DateList: RowData = str(RowData)[0:19] 
                qrySelect = qrySelect + "'" + str(RowData) + "' AS " + ColumnName +', ' 
            qrySelect1  = qrySelect[0:(len(qrySelect)-2)]; qryInsert1  = qryInsert[0:(len(qryInsert)-2)]
            qryLoadData = f'INSERT INTO {TableName} (' + qryInsert1 + ') Select ' + qrySelect1 
            # print(qryLoadData);input()
            Cursor = ConnectToODSServer().ODSConnection.cursor()
            Cursor.execute(qryLoadData); Cursor.commit()
            ConnectToODSServer().ODSConnection.close()
