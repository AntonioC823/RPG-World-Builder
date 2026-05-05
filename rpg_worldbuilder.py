"""
RPG Worldbuilder
Milestone #1

Main pages:
1. Login Page
2. Load/Create RPG Page
3. Create/Edit Character Page
4. Generate/Edit World Page
5. View World Page
6. Help Page
"""

import tkinter as tk
import json
import os

from login_page import LoginPage
from load_create_page import LoadCreatePage
from character_page import CharacterPage
from world_page import WorldPage
from view_world_page import ViewWorldPage
from help_page import HelpPage


class RPGWorldbuilder:
    """
    Main application controller class. Initializes all pages, stores shared data, and handles switching between pages.
    """

    def __init__(self, root):
        """
        Initialize the application.
        """
        self.root = root
        self.root.title("RPG Worldbuilder")
        self.root.geometry("1280x720")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Shared data across pages
        self.character = {}
        self.world = {}

        # Store all pages
        self.pages = {}
        for Page in (LoginPage, LoadCreatePage, CharacterPage, WorldPage, ViewWorldPage, HelpPage):
            page = Page(self.root, self)
            self.pages[Page.__name__] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.users_file = "users.json"
        self.users = self.load_users()

        self.current_user = None
        self.current_world_name = None

        self.world_file = "worlds.json"
        self.saved_worlds = self.load_worlds()

        # Start with Login Page
        self.show_page("LoginPage")

    def show_page(self, page_name):
        """
        Display the requested page.
        """
        self.pages[page_name].tkraise()

        if page_name == "ViewWorldPage":
            self.pages[page_name].refresh_view()

        if page_name == "LoadCreatePage":
            self.pages[page_name].update_world_list()
            self.pages[page_name].update_recent_worlds()

    def load_users(self):
        """
        Load saved usernames and passwords from a local JSON file.
        """
        if os.path.exists(self.users_file):
            with open(self.users_file, "r") as file:
                return json.load(file)
            
        return {}


    def save_users(self):
        """
        Save usernames and passwords to a local JSON file.
        """
        with open(self.users_file, "w") as file:
            json.dump(self.users, file, indent=4)

    
    def load_worlds(self):
        """
        Load saved worlds from a local JSON file.
        """
        if os.path.exists(self.world_file):
            with open(self.world_file, "r") as file:
                return json.load(file)
        return {}

    
    def save_worlds(self):
        """
        Save worlds to a local JSON file.
        """
        with open(self.world_file, "w") as file:
            json.dump(self.saved_worlds, file, indent=4)

    
    def show_error_popup(self, message, title="Error"):
        """
        Displays a popup for error messages.
        """
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("400x150")
        popup.resizable(False, False)

        # Center popup relative to main window
        self.root.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 200
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 75
        popup.geometry(f"400x150+{x}+{y}")

        tk.Label(
            popup,
            text=message,
            font=("Arial", 12),
            wraplength=350,
            justify="center"
        ).pack(pady=25)

        tk.Button(
            popup,
            text="OK",
            width=12,
            command=popup.destroy
        ).pack()

        popup.transient(self.root)
        popup.grab_set()


if __name__ == "__main__":
    root = tk.Tk()
    app = RPGWorldbuilder(root)
    root.mainloop()