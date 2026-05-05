import tkinter as tk

class HelpPage(tk.Frame):
    """
    Help page.
    """

    def __init__(self, parent, controller):
        """
        Initialize help page widgets.
        """
        super().__init__(parent, bg="#f4f4f4")
        self.controller = controller

        container = tk.Frame(self, bg="#f4f4f4")
        container.place(relx=0.5, rely=0.5, anchor="center")

        # Navigation bar
        nav_frame = tk.Frame(self, bg="#dddddd")
        nav_frame.pack(fill="x")

        tk.Button(
            nav_frame,
            text="Load/Create RPG",
            font=("Arial", 11),
            command=lambda: controller.show_page("LoadCreatePage")
        ).pack(side="left", padx=10, pady=8)

        tk.Button(
            nav_frame,
            text="Create/Edit Character",
            font=("Arial", 11),
            command=lambda: controller.show_page("CharacterPage")
        ).pack(side="left", padx=10, pady=8)

        tk.Button(
            nav_frame,
            text="Generate/Edit World",
            font=("Arial", 11),
            command=lambda: controller.show_page("WorldPage")
        ).pack(side="left", padx=10, pady=8)

        tk.Button(
            nav_frame,
            text="View World",
            font=("Arial", 11),
            command=lambda: controller.show_page("ViewWorldPage")
        ).pack(side="left", padx=10, pady=8)

        tk.Label(
            container,
            text="Help Page",
            font=("Arial", 32),
            bg="#f4f4f4"
        ).pack(pady=(45, 20))

        help_text = (
            "1. Login Page:\n"
            "   Enter your username and password to access your saved RPG worlds. "
            "If you are a new user, create an account to get started.\n\n"

            "2. Load/Create RPG:\n"
            "   Search for existing RPG worlds using the search bar or dropdown list. "
            "You can also create a new RPG build from scratch. "
            "Recently created worlds will appear at the bottom for quick access.\n\n"

            "3. Create/Edit Character:\n"
            "   Enter a character name, select a class, and choose exactly 3 attributes. "
            "Make sure to save your character before leaving the page, or your changes may be lost.\n\n"

            "4. Generate/Edit World:\n"
            "   Enter a world name, select a world type, and choose exactly 5 features. "
            "Saving will store your world along with the current character.\n\n"

            "5. View World:\n"
            "   Review your saved character and world details. "
            "You can refresh the page to ensure the latest information is displayed.\n\n"

            "6. Logout:\n"
            "   Use the logout button when you are finished. "
            "You will be asked to confirm before exiting, and unsaved changes will be lost."
        )

        tk.Label(
            container,
            text=help_text,
            font=("Arial", 14),
            justify="left",
            bg="#f4f4f4",
            wraplength=800
        ).pack(pady=20)

        tk.Button(
            container,
            text="Logout",
            width=25,
            font=("Arial", 12),
            command=self.logout_with_warning
        ).pack(pady=6)


    def logout_with_warning(self):
        """
        Ask the user to confirm logout.
        """
        popup = tk.Toplevel(self.controller.root)
        popup.title("Confirm Logout")
        popup.geometry("420x180")
        popup.resizable(False, False)

        self.controller.root.update_idletasks()
        x = self.controller.root.winfo_x() + (self.controller.root.winfo_width() // 2) - 210
        y = self.controller.root.winfo_y() + (self.controller.root.winfo_height() // 2) - 90
        popup.geometry(f"420x180+{x}+{y}")

        tk.Label(
            popup,
            text="Are you sure you want to logout?",
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
            command=lambda: self.confirm_logout(popup)
        ).pack(side="left", padx=10)

        tk.Button(
            button_frame,
            text="No",
            width=10,
            command=popup.destroy
        ).pack(side="left", padx=10)

        popup.transient(self.controller.root)
        popup.grab_set()


    def confirm_logout(self, popup):
        """
        Confirm logout and return to login page.
        """
        popup.destroy()
        self.controller.show_page("LoginPage")