from flet import *
import bcrypt as bc
import SYSConnectToServers as CS
import GUILandingPage as GLP


class LoginScreen(Container):

    def __init__(self, page):
        super().__init__()
        
        self.page = page
        self.ODS = CS.ConnectToODSServer()
        self.salt = bc.gensalt()
        self.GetLoginScreen()
        self.LoginScreen =  Container(expand=True,content=Row(controls=[(Column([self.username, self.password, self.signup, self.submit],
                            alignment=MainAxisAlignment.CENTER))],alignment=MainAxisAlignment.CENTER))

    # input fields for login and pswd 

    def GetLoginScreen(self):
        self.username = TextField(border_color="#AD1457", label='Username',color='white', text_align=TextAlign.LEFT, height=40, width=200)
        self.password = TextField(border_color="#AD1457", label='Password', color='white', text_align=TextAlign.LEFT,height=40, width=200,
                        password=True, can_reveal_password=True)
        self.signup = Container(height=20)
        # self.submit = ElevatedButton(text='Login', bgcolor="#AD1457", color='white', height=40, width=200, on_click=self.GetSubmit, disabled=False)
        self.submit = ElevatedButton(text='Login', bgcolor="#AD1457", color='white', height=40, width=200, on_click=self.GetSubmit)

    # pswd validation     

    async def GetSubmit(self, e):
        # StoredPsswd = str(self.ODS.qryODSGetData(f"select HashedPassword from ETLUserData where UserName = '{self.username.value}'").values[0][0]); self.ODS.ODSConnection.close
        # StoredPsswd = StoredPsswd.encode("utf-8")
        # EnteredPsswd = self.password.value.encode("utf-8")
        # if bc.checkpw(EnteredPsswd, StoredPsswd): await self.PageRoute()
        # else: print("Password is Incorrect")
        await self.PageRoute()

    # route page to landingpage

    async def PageRoute(self):
        await self.page.clean_async()
        await self.page.go_async('/ForwardReporting')
        await self.page.add_async(GLP.LandingPage(self.page).HomeScreen)
        await self.page.update_async()



















