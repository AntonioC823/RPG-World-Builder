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
            self.pages[page_name].update_user_stats()


    def logout(self, popup):
        """
        Close the popup and return to the login page.
        """
        popup.destroy()
        self.show_page("LoginPage")


    def confirm_navigation(self, popup, page_name):
        """
        Close the popup and navigate to the requested page.
        """
        popup.destroy()
        self.show_page(page_name)


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


    def center_popup(self, popup, width, height):
        """
        Center a popup window relative to the main application window.
        """
        self.root.update_idletasks()

        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (width // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (height // 2)

        popup.geometry(f"{width}x{height}+{x}+{y}")


    def show_confirm_popup(self, message, title, on_yes, width=420, height=180):
        """
        Display a confirmation popup with Yes and No buttons.
        """
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry(f"{width}x{height}")
        popup.resizable(False, False)

        self.center_popup(popup, width, height)

        tk.Label(
            popup,
            text=message,
            font=("Arial", 12),
            wraplength=360,
            justify="center"
        ).pack(pady=25)

        button_frame = tk.Frame(popup)
        button_frame.pack(pady=5)

        tk.Button(
            button_frame,
            text="Yes",
            width=10,
            command=lambda: on_yes(popup)
        ).pack(side="left", padx=10)

        tk.Button(
            button_frame,
            text="No",
            width=10,
            command=popup.destroy
        ).pack(side="left", padx=10)

        popup.transient(self.root)
        popup.grab_set()

    
    def show_message_popup(self, message, title="Message"):
        """
        Display a simple popup message with an OK button.
        """
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("400x150")
        popup.resizable(False, False)

        self.center_popup(popup, 400, 150)

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


    def show_error_popup(self, message, title="Error"):
        """
        Display an error or status popup.
        """
        self.show_message_popup(message, title)


if __name__ == "__main__":
    root = tk.Tk()
    app = RPGWorldbuilder(root)
    root.mainloop()