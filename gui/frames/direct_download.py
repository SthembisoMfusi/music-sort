import customtkinter
from logic.downloader import Downloader

class DirectDownloadFrame(customtkinter.CTkFrame):
    """
    Frame for Direct Utility actions.
    
    Allows the user to paste a Spotify Link (Song/Album/Playlist) directly.
    Displays a real-time console log of the download process.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.controller = controller
        self.downloader = Downloader()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1) # Console expands

        self.title = customtkinter.CTkLabel(self, text="Direct Download", font=customtkinter.CTkFont(size=24, weight="bold"))
        self.title.grid(row=0, column=0, padx=20, pady=20)

        self.url_entry = customtkinter.CTkEntry(self, placeholder_text="Paste Spotify URL (Song, Album, Playlist, Podcast)")
        self.url_entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.download_btn = customtkinter.CTkButton(self, text="Download", command=self.start_download)
        self.download_btn.grid(row=2, column=0, padx=20, pady=20)

        self.console = customtkinter.CTkTextbox(self, width=600, height=300)
        self.console.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")

    def set_url(self, url):
        self.url_entry.delete(0, "end")
        self.url_entry.insert(0, url)

    def start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            return
        
        self.download_btn.configure(state="disabled", text="Downloading...")
        self.console.delete("0.0", "end")
        
        # Start download using logic class
        self.downloader.download(
            url, 
            output_callback=self.append_console, 
            finish_callback=self.on_download_finish
        )

    def append_console(self, text):
        # Must be thread-safe for tkinter
        self.after(0, lambda: self.console.insert("end", text))
        self.after(0, lambda: self.console.see("end"))

    def on_download_finish(self, success, message):
        self.append_console(f"\n{message}\n")
        self.after(0, lambda: self.download_btn.configure(state="normal", text="Download"))
