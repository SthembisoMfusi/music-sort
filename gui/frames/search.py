import customtkinter
from tkinter import messagebox
from logic.spotify_helper import SpotifyHelper
import os

class SearchFrame(customtkinter.CTkFrame):
    """
    Frame for searching and browsing Spotify tracks.
    
    Displays a search bar and a scrollable list of results.
    Each result card allows triggering a download for that specific song or its album.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.title = customtkinter.CTkLabel(self, text="Search Spotify", font=customtkinter.CTkFont(size=24, weight="bold"))
        self.title.grid(row=0, column=0, padx=20, pady=20)
        
        self.info = customtkinter.CTkLabel(self, text="Search requires API keys in Settings.", text_color="gray")
        self.info.grid(row=1, column=0, padx=20, pady=(0,20))

        self.search_entry = customtkinter.CTkEntry(self, placeholder_text="Enter song or artist...")
        self.search_entry.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.search_btn = customtkinter.CTkButton(self, text="Search", command=self.perform_search)
        self.search_btn.grid(row=3, column=0, padx=20, pady=10)

        self.results_area = customtkinter.CTkScrollableFrame(self, label_text="Results")
        self.results_area.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")

    def perform_search(self):
        cid = os.getenv("SPOTIPY_CLIENT_ID")
        secret = os.getenv("SPOTIPY_CLIENT_SECRET")
        
        if not cid or not secret:
            messagebox.showerror("Missing Keys", "Please configure Client ID and Secret in Settings tab first.")
            return

        query = self.search_entry.get().strip()
        if not query:
            return

        try:
            helper = SpotifyHelper(cid, secret)
            tracks = helper.search_track(query)
            self.display_results(tracks)
        except Exception as e:
            messagebox.showerror("Search Error", str(e))

    def display_results(self, tracks):
        # Clear previous
        for widget in self.results_area.winfo_children():
            widget.destroy()

        for track in tracks:
            self.create_result_card(track)

    def create_result_card(self, track):
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        album_name = track['album']['name']
        track_url = track['external_urls']['spotify']
        album_url = track['album']['external_urls']['spotify']

        card = customtkinter.CTkFrame(self.results_area)
        card.pack(fill="x", padx=5, pady=5)
        
        label_text = f"{track_name}\n{artist_name} - {album_name}"
        lbl = customtkinter.CTkLabel(card, text=label_text, anchor="w", justify="left")
        lbl.pack(side="left", padx=10, pady=10, expand=True)
        
        # Download Song
        btn_dl_song = customtkinter.CTkButton(card, text="DL Song", width=80, 
                                              command=lambda u=track_url: self.trigger_download(u))
        btn_dl_song.pack(side="right", padx=5)
        
        # Download Album
        btn_dl_album = customtkinter.CTkButton(card, text="DL Album", width=80, fg_color="green",
                                               command=lambda u=album_url: self.trigger_download(u))
        btn_dl_album.pack(side="right", padx=5)

    def trigger_download(self, url):
        # Use controller to switch tabs and start download
        self.controller.show_direct_download(url)
