from flet import *
import SYSConnectToServers as CS
import pandas as pd
import GUIForm as GF

class FormAddScreen(Container):

    def __init__(self, page, Query, ScreenName, ReportTitle):
        super().__init__()

        self.page = page
        self.ODS = CS.ConnectToODSServer()
        self.ColumnNames = []; self.RowsData = []; self.RowValues = ''
        self.ScreenName = ScreenName; self.ReportTitle = ReportTitle; self.Query = Query
        self.TableData = pd.DataFrame(self.ODS.qryODSGetData(self.Query)); self.ODS.ODSConnection.close; self.GetRefineTableData()
        self.FormScreen = Column(expand=True, controls=[])

    # refine table data for form fields

    def GetRefineTableData(self):
        print(self.ScreenName, self.ReportTitle)
        if self.ScreenName == 'BrdxVariablesScreen': self.TableData = self.TableData.drop(['UID','CONID','Identifier','ProductCode','DWSource','Description'], axis=1)
        elif self.ScreenName == 'BrdxTemplates': self.TableData = self.TableData.drop(['UID','CONID'], axis=1)

    # create addFormScreen and option buttons 
        
    def GetFormAddScreen(self):
        self.FormFields = Container(expand=True,height=150,bgcolor="white10",border=border.all(1,"#ebebeb"),border_radius=8,padding=15,
                        content=Column(expand=True,controls=[Row(expand=True,controls=self.GetFormFields()),
                        Divider(height=2,color="transparent"),Row(expand=True,alignment=MainAxisAlignment.END,controls=[self.GetFormButton()])]))
        self.FormHeader = Container(expand=True, height=50, bgcolor="#AD1457",border_radius=border_radius.only(top_left=15,top_right=15),
                        padding=padding.only(left=15,right=15),content=Row(expand=True,alignment=MainAxisAlignment.SPACE_BETWEEN,
                        controls=[IconButton(icon=icons.NAVIGATE_BEFORE_ROUNDED,icon_color=colors.WHITE, on_click = self.GetNavigateBack),
                            Container(expand=True,content=Text(self.ReportTitle,text_align="left",size=18,color="white",weight='bold'))]))  
        self.ReportScreen = Column(expand=True,controls=[Row(expand = False, controls=[self.FormHeader]), Row(expand = False, controls=[self.FormFields])])
        self.FormScreen.controls.append(self.ReportScreen)
        return self.FormScreen
    
    # create add form fields
    
    def GetFormFields(self):
        TableFrameColumns = self.TableData.columns; ColumnNames = []; counter = 0
        for cols in TableFrameColumns:
            ColumnNames.append(Container(expand=2,height=45,bgcolor="#ebebeb",border_radius=6,padding=8,content=Column(spacing=1,controls=[
                Text(value=f'{cols}',size=9,color="black",weight="bold"),TextField(border_color="transparent",height=20,text_size=13,
                content_padding=0,cursor_color="black",cursor_width=1,cursor_height=18,color="black")])))
            counter = counter + 1
        return ColumnNames
    
    # handle navigate back events
    
    async def GetNavigateBack(self, e):
        print(self.ScreenName)
        self.ReportScreen = GF.FormScreen(self.page, self.Query, self.ScreenName, self.ReportTitle).GetFormScreen()
        self.FormScreen.controls.clear()
        self.FormScreen.controls.append(self.ReportScreen)
        await self.FormScreen.update_async()

    # create add form buttons

    def GetFormButton(self):
        FormButton = Container(alignment=alignment.center,content= Row(controls=[
            ElevatedButton(on_click=[],bgcolor="#AD1457",color="white",content=Row(controls=[Icon(name=icons.ADD_ROUNDED,size=12, color=colors.WHITE),
                    Text("Commit", size=10, weight="bold")]),style=ButtonStyle(shape={"":RoundedRectangleBorder(radius=6)},color={"":"white"}),height=30,width=100)]))
        return FormButton
        