"""
Entry Point for SpotDL GUI Manager.
Initializes the CustomTkinter appearance and launches the main application loop.
"""
import customtkinter
from gui.app import App

if __name__ == "__main__":
    customtkinter.set_appearance_mode("Dark")
    customtkinter.set_default_color_theme("blue")
    
    app = App()
    app.mainloop()
