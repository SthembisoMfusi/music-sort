import customtkinter
import os
from tkinter import messagebox

class SettingsFrame(customtkinter.CTkFrame):
    """
    Frame for Application Settings.
    
    Currently handles the input and storage of Spotify Client ID and Client Secret
    variables, which are saved to a local .env file.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=1)
        
        self.title = customtkinter.CTkLabel(self, text="Settings", font=customtkinter.CTkFont(size=24, weight="bold"))
        self.title.grid(row=0, column=0, padx=20, pady=20)
        
        self.info = customtkinter.CTkLabel(self, text="Spotify Developer Credentials.\nRequired for Search functionality.", text_color="gray")
        self.info.grid(row=1, column=0, padx=20, pady=(0,20))

        self.entry_cid = customtkinter.CTkEntry(self, placeholder_text="Client ID")
        self.entry_cid.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        self.entry_secret = customtkinter.CTkEntry(self, placeholder_text="Client Secret", show="*")
        self.entry_secret.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.save_btn = customtkinter.CTkButton(self, text="Save Credentials", command=self.save_credentials)
        self.save_btn.grid(row=4, column=0, padx=20, pady=20)
        
        self.load_initial_values()

    def load_initial_values(self):
        # We can ask the controller for current env vars
        cid = os.getenv("SPOTIPY_CLIENT_ID") or ""
        secret = os.getenv("SPOTIPY_CLIENT_SECRET") or ""
        self.entry_cid.insert(0, cid)
        self.entry_secret.insert(0, secret)

    def save_credentials(self):
        cid = self.entry_cid.get().strip()
        secret = self.entry_secret.get().strip()
        
        # Save to .env
        try:
            with open(".env", "w") as f:
                f.write(f"SPOTIPY_CLIENT_ID={cid}\n")
                f.write(f"SPOTIPY_CLIENT_SECRET={secret}\n")
            
            # Update runtime env
            os.environ["SPOTIPY_CLIENT_ID"] = cid
            os.environ["SPOTIPY_CLIENT_SECRET"] = secret
            
            messagebox.showinfo("Saved", "Credentials saved locally to .env file.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save .env: {e}")
