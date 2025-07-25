from flet import *
import flet_fastapi
import GUILoginScreen as GLS


class MainPage(Container):

    def __init__(self, page):
        super().__init__()

        self.page = page
        self.FileSelector = FilePicker(on_result=self.SelectFiles)
        self.page.overlay.append(self.FileSelector)
        self.FileSelect =  ElevatedButton("Load Template...",icon=icons.FOLDER_OPEN, on_click=self.FileSelector.pick_files,visible=False)

    # file select for desktop apps only

    def SelectFiles(self, e: FilePickerResultEvent):
        if e.files is not None: print( e.files)

# call login page 

async def root_main(page: Page):
    page.theme_mode = "dark"
    PageOption = MainPage(page).FileSelect
    await page.add_async(GLS.LoginScreen(page).LoginScreen, PageOption)
    await page.update_async()


app = flet_fastapi.FastAPI()

app.mount("/", flet_fastapi.app(root_main))