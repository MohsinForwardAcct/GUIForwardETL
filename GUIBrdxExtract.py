
import SYSConnectToServers as CS
import pandas as pd
from flet import *

class DownloadBrdxReport():

    def __init__(self):
        
        self.ODS = CS.ConnectToODSServer()
        self.ETL = CS.ConnectToETLServer()
        self.GetQueryBuild()

    # generate BrdxTemplate 
    
    async def GetBrdxTemplate(self, CONID):
        LogicData = pd.DataFrame(self.ODS.qryODSGetData(f"Select * from RESVBrdxReportTemplates where CONID = '{CONID}' order by ColumnSequence"))
        self.ODS.ODSConnection.close
        self.ETL.qryETLAppendData(f"if OBJECT_ID (N'tempBrdxDownloadFinal', N'U') IS NOT NULL drop table tempBrdxDownloadFinal")
        self.ETL.ETLConnection.close
        qryCreateTemplate = ""
        for index, BrdxRows in LogicData.iterrows():
            ColumnName=BrdxRows["ColumnOutput"]; DataType=BrdxRows["DataType"]; AllowNull=BrdxRows["AllowNull"]
            qryCreateTemplate = qryCreateTemplate + " [" + (ColumnName) + "] " + (DataType) + " " + AllowNull + ", "
        qryCreateTemplate  = qryCreateTemplate[0:(len(qryCreateTemplate)-2)]   
        qryCreateTemplate = f"Create table tempBrdxDownloadFinal ({qryCreateTemplate})" 
        # print(qryCreateTemplate); input()
        self.ETL.qryETLAppendData(qryCreateTemplate)
        self.ETL.ETLConnection.close

    # generate brdx report 

    async def GetBrdxDownloadData(self, ReportingYear, ReportingPeriod, CONID, PremiumCategory, ProductCode, ContractNumber):   
        qrySelect = ''; qryInsert = ''
        LogicData = pd.DataFrame(self.ODS.qryODSGetData(query = f"Select * from RESVBrdxReportVariables where CONID = '{CONID}' and ProductCode = '{ProductCode}'"))
        self.ODS.ODSConnection.close
        for index, BrdxRows in LogicData.iterrows():
            ColumnName=BrdxRows["ColumnOutput"]; TableName=BrdxRows["TableName"]; ColumnValue=BrdxRows["Variables"]
            qrySelect = qrySelect + " [" + (ColumnName) + "], "
            if TableName == 'DIMManualData': qryInsert = qryInsert + "'" + str(ColumnValue) + "' AS [" + ColumnName +'], ' 
            elif TableName == 'Function': qryInsert = qryInsert + str(ColumnValue) + " AS [" + ColumnName +'], ' 
            else: qryInsert = qryInsert + "dbo." + str(TableName) + "." + str(ColumnValue) + " AS [" + ColumnName +'], '
        qrySelect1  = qrySelect[0:(len(qrySelect)-2)]; qryInsert1  = qryInsert[0:(len(qryInsert)-2)]
        qryWhere = f" WHERE dbo.FACTData.ReportingPeriod='{ReportingPeriod}' AND dbo.FACTData.ContractNumber='{ContractNumber}' AND dbo.FACTData.CONID='{CONID}' \
            AND dbo.FACTData.ProductCode='{ProductCode}' AND dbo.FACTData.PremiumCategory='{PremiumCategory}';"   
        qryLoadData = f'INSERT INTO tempBrdxDownloadFinal (' + qrySelect1 + ') Select ' + qryInsert1 + self.qryRelation + qryWhere
        # print(qryLoadData);input() 
        self.ETL.qryETLAppendData(qryLoadData)
        self.ETL.ETLConnection.close

    # generate brdx query built 

    def GetQueryBuild(self):
        self.qryRelation = f" FROM dbo.DIMALISReconData RIGHT JOIN (dbo.DIMLiabilityData RIGHT JOIN (dbo.DIMAddressData RIGHT JOIN (dbo.DIMEQData \
            RIGHT JOIN (dbo.DIMTIVData RIGHT JOIN (dbo.DIMPremiumData RIGHT JOIN (dbo.DIMSharePrcntData RIGHT JOIN (dbo.DIMContractData \
            RIGHT JOIN (dbo.DIMJETData RIGHT JOIN (dbo.FACTData LEFT JOIN dbo.DIMBrdxData ON dbo.FACTData.UID = dbo.DIMBrdxData.UID) \
            ON dbo.DIMJETData.UID = dbo.FACTData.UID) ON dbo.DIMContractData.UID = dbo.FACTData.UID) ON dbo.DIMSharePrcntData.UID = dbo.FACTData.UID) \
            ON dbo.DIMPremiumData.UID = dbo.FACTData.UID) ON dbo.DIMTIVData.UID = dbo.FACTData.UID) ON dbo.DIMEQData.UID = dbo.FACTData.UID) \
            ON dbo.DIMAddressData.UID = dbo.FACTData.UID) ON dbo.DIMLiabilityData.UID = dbo.FACTData.UID) ON dbo.DIMALISReconData.UID = dbo.FACTData.UID"


