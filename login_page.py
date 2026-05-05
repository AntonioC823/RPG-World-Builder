import tkinter as tk

class LoginPage(tk.Frame):
    """
    Login page.
    """

    def __init__(self, parent, controller):
        """
        Initialize login page widgets.
        """
        super().__init__(parent, bg="#f4f4f4")
        self.controller = controller

        container = tk.Frame(self, bg="#f4f4f4")
        container.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            container,
            text="RPG Worldbuilder",
            font=("Arial", 32),
            bg="#f4f4f4"
        ).pack(pady=20)

        tk.Label(
            container,
            text="Create RPG worlds, characters, and stories.",
            font=("Arial", 14),
            bg="#f4f4f4"
        ).pack(pady=10)

        tk.Label(container, text="Username", font=("Arial", 14), bg="#f4f4f4").pack(pady=5)
        self.username = tk.Entry(container, width=35, font=("Arial", 12))
        self.username.pack(pady=5)

        tk.Label(container, text="Password", font=("Arial", 14), bg="#f4f4f4").pack(pady=5)
        self.password = tk.Entry(container, width=35, font=("Arial", 12), show="*")
        self.password.pack(pady=5)

        tk.Button(
            container,
            text="Login",
            width=25,
            font=("Arial", 12),
            command=self.login
        ).pack(pady=20)

        tk.Button(
            container,
            text="Create Account",
            width=25,
            font=("Arial", 12),
            command=self.create_account
        ).pack(pady=5)

    def login(self):
        """
        Allow the user to log in only if the account exists.
        """
        username = self.username.get().strip()
        password = self.password.get().strip()

        if username == "" or password == "":
            self.controller.show_error_popup("Please enter both username and password or create an account.", "Login Error")
            return

        if username not in self.controller.users:
            self.controller.show_error_popup("Account not found. Please create an account first.", "Login Error")
            return

        if self.controller.users[username] != password:
            self.controller.show_error_popup("Incorrect password. Please try again.", "Login Error")
            return
        
        self.controller.current_user = username

        # Load world
        if username in self.controller.saved_worlds:
            self.controller.world = self.controller.saved_worlds[username]

            # If world has a character, sync it
            if "character" in self.controller.world:
                self.controller.character = self.controller.world["character"]
        else:
            self.controller.world = {}
            self.controller.character = {}

        self.controller.show_page("LoadCreatePage")

    def create_account(self):
        """
        Create and save a new username and password.
        """
        username = self.username.get().strip()
        password = self.password.get().strip()

        if username == "" or password == "":
            self.controller.show_error_popup("Please enter both username and password before creating an account.", "Create Account Error")
            return

        if username in self.controller.users:
            self.controller.show_error_popup("This username already exists. Please log in or choose another username.", "Create Account Error")
            return

        self.controller.users[username] = password
        self.controller.save_users()

        self.controller.show_error_popup("Account created successfully. You can now log in.", "Account Created")