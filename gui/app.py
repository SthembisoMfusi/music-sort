import customtkinter
import dotenv
from gui.frames.search import SearchFrame
from gui.frames.direct_download import DirectDownloadFrame
from gui.frames.settings import SettingsFrame

class App(customtkinter.CTk):
    """
    Main Application Controller.
    
    This class manages the main window, sidebar navigation, and switches between 
    different functional frames (Search, Direct Download, Settings).
    It also acts as a central coordinator, allowing frames to communicate (e.g., Search triggering a Download).
    """
    def __init__(self):
        super().__init__()

        # Configuration
        self.title("SpotDL GUI Manager")
        self.geometry("900x600")
        
        dotenv.load_dotenv()
        
        # Grid Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Sidebar
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="SpotDL Manager", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_btn_search = customtkinter.CTkButton(self.sidebar_frame, text="Search Music", command=self.show_search)
        self.sidebar_btn_search.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_btn_direct = customtkinter.CTkButton(self.sidebar_frame, text="Direct Download", command=self.show_direct)
        self.sidebar_btn_direct.grid(row=2, column=0, padx=20, pady=10)

        self.sidebar_btn_settings = customtkinter.CTkButton(self.sidebar_frame, text="Settings", command=self.show_settings)
        self.sidebar_btn_settings.grid(row=3, column=0, padx=20, pady=10)
        
        # Appearance Mode
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance)
        self.appearance_mode_menu.grid(row=7, column=0, padx=20, pady=(10, 20))
        self.appearance_mode_menu.set("Dark")

        # Frames
        self.search_frame = SearchFrame(self, controller=self)
        self.direct_frame = DirectDownloadFrame(self, controller=self)
        self.settings_frame = SettingsFrame(self, controller=self)
        
        self.frames = {
            "search": self.search_frame,
            "direct": self.direct_frame,
            "settings": self.settings_frame
        }
        
        self.show_direct()

    def change_appearance(self, new_mode):
        customtkinter.set_appearance_mode(new_mode)

    def _show_frame(self, name):
        for frame in self.frames.values():
            frame.grid_forget()
        self.frames[name].grid(row=0, column=1, sticky="nsew")

    def show_search(self):
        self._show_frame("search")

    def show_direct(self):
        self._show_frame("direct")

    def show_settings(self):
        self._show_frame("settings")

    def show_direct_download(self, url):
        """
        Public method to switch to Direct Download tab and pre-fill URL.
        """
        self.show_direct()
        self.direct_frame.set_url(url)
        self.direct_frame.start_download()
