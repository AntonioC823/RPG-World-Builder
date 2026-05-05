import tkinter as tk
import random

class WorldPage(tk.Frame):
    """
    Generate/Edit World page.
    """

    def __init__(self, parent, controller):
        """
        Initialize world page widgets.
        """
        super().__init__(parent, bg="#f4f4f4")
        self.controller = controller

        self.unsaved_changes = False

        # Navigation bar
        nav_frame = tk.Frame(self, bg="#dddddd")
        nav_frame.pack(fill="x")

        tk.Button(
            nav_frame,
            text="Load/Create RPG",
            font=("Arial", 11),
            command=lambda: self.navigate_with_warning("LoadCreatePage")
        ).pack(side="left", padx=10, pady=8)

        tk.Button(
            nav_frame,
            text="Create/Edit Character",
            font=("Arial", 11),
            command=lambda: self.navigate_with_warning("CharacterPage")
        ).pack(side="left", padx=10, pady=8)

        tk.Button(
            nav_frame,
            text="View World",
            font=("Arial", 11),
            command=lambda: self.navigate_with_warning("ViewWorldPage")
        ).pack(side="left", padx=10, pady=8)

        container = tk.Frame(self, bg="#f4f4f4")
        container.place(relx=0.5, rely=0.55, anchor="center")

        tk.Label(
            container,
            text="Generate/Edit World",
            font=("Arial", 32),
            bg="#f4f4f4"
        ).pack(pady=(20, 5))

        tk.Label(
            container,
            text="Enter world details below.",
            font=("Arial", 14),
            bg="#f4f4f4"
        ).pack(pady=0)

        tk.Label(container, text="World Name", font=("Arial", 14), bg="#f4f4f4").pack(pady=5)
        self.name = tk.Entry(container, width=35, font=("Arial", 12))
        self.name.pack(pady=5)

        self.name.bind("<KeyRelease>", self.mark_unsaved)

        # World Type selection
        tk.Label(
            container,
            text="Choose a World Type",
            font=("Arial", 14),
            bg="#f4f4f4"
        ).pack(pady=10)

        self.world_type = tk.StringVar()
        self.world_type.set("NONE")

        type_frame = tk.Frame(container, bg="#f4f4f4")
        type_frame.pack(pady=5)

        world_types = [
            "Fantasy Kingdom", "Dark Fantasy", "Sci-Fi Galaxy", "Post-Apocalyptic",
            "Medieval Realm", "Cyberpunk City", "Steampunk World",
            "Mythological Realm", "Magical Academy", "Horror Realm"
        ]

        for index, wtype in enumerate(world_types):
            tk.Radiobutton(
                type_frame,
                text=wtype,
                variable=self.world_type,
                value=wtype,
                font=("Arial", 11),
                bg="#f4f4f4",
                command=self.mark_unsaved
            ).grid(row=index // 5, column=index % 5, sticky="w", padx=10, pady=5)

        # World Features selection
        tk.Label(
            container,
            text="Choose 5 World Features",
            font=("Arial", 14),
            bg="#f4f4f4"
        ).pack(pady=10)

        self.feature_vars = {}

        features = [
            "Magic System", "Advanced Technology", "Ancient Ruins",
            "Hidden Treasures", "Dangerous Creatures", "Political Conflict",
            "Guilds & Factions", "Mystical Artifacts", "Harsh Environment",
            "Time Travel"
        ]

        feature_frame = tk.Frame(container, bg="#f4f4f4")
        feature_frame.pack(pady=5)

        for index, feature in enumerate(features):
            var = tk.BooleanVar()
            self.feature_vars[feature] = var

            tk.Checkbutton(
                feature_frame,
                text=feature,
                variable=var,
                font=("Arial", 11),
                bg="#f4f4f4",
                command=self.feature_changed
            ).grid(row=index // 5, column=index % 5, sticky="w", padx=10, pady=5)

        tk.Button(
            container,
            text="Generate World",
            width=25,
            font=("Arial", 12),
            command=self.generate_world
        ).pack(pady=10)

        tk.Button(
            container,
            text="Save World",
            width=25,
            font=("Arial", 12),
            command=self.save_world
        ).pack(pady=20)

        tk.Button(
            container,
            text="Logout",
            width=25,
            font=("Arial", 12),
            command=self.logout_with_warning
        ).pack(pady=6)

        tk.Button(
            container,
            text="Help",
            width=25,
            font=("Arial", 12),
            command=lambda: self.navigate_with_warning("HelpPage")
        ).pack(pady=6)

    def get_selected_features(self):
        """
        Return a list of selected world features.
        """
        return [f for f, var in self.feature_vars.items() if var.get()]


    def limit_features(self):
        """
        Prevent selecting more than 5 features.
        """
        selected = self.get_selected_features()

        if len(selected) > 5:
            self.controller.show_error_popup("You can only choose up to 5 features.", "Feature Selection Error")

            # Uncheck last selected
            for f, var in self.feature_vars.items():
                if var.get() and f == selected[-1]:
                    var.set(False)
                    break

    def mark_unsaved(self, event=None):
        """
        Mark the world page as having unsaved changes.
        """
        self.unsaved_changes = True


    def feature_changed(self):
        """
        Mark changes and enforce the feature limit.
        """
        self.mark_unsaved()
        self.limit_features()


    def navigate_with_warning(self, page_name):
        """
        Warn the user before leaving the page if there are unsaved changes.
        """
        if self.unsaved_changes:
            popup = tk.Toplevel(self.controller.root)
            popup.title("Unsaved Changes")
            popup.geometry("400x150")
            popup.resizable(False, False)

            # Center popup relative to main window
            self.controller.root.update_idletasks()
            x = self.controller.root.winfo_x() + (self.controller.root.winfo_width() // 2) - 210
            y = self.controller.root.winfo_y() + (self.controller.root.winfo_height() // 2) - 90
            popup.geometry(f"400x150+{x}+{y}")

            tk.Label(
                popup,
                text="All unsaved changes will be lost.\nAre you sure you want to leave this page?",
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
                command=lambda: self.confirm_navigation(page_name, popup)
            ).pack(side="left", padx=10)

            tk.Button(
                button_frame,
                text="No",
                width=10,
                command=popup.destroy
            ).pack(side="left", padx=10)

            popup.transient(self.controller.root)
            popup.grab_set()
        else:
            self.controller.show_page(page_name)


    def confirm_navigation(self, page_name, popup):
        """
        Confirm navigation away from the page.
        """
        self.unsaved_changes = False
        popup.destroy()
        self.controller.show_page(page_name)


    def logout_with_warning(self):
        """
        Ask the user to confirm logout. Warn about unsaved changes if needed.
        """
        message = "Are you sure you want to logout?"

        if self.unsaved_changes:
            message = "Are you sure you want to logout?\nAll unsaved changes will be lost."

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
        self.unsaved_changes = False
        popup.destroy()
        self.controller.show_page("LoginPage")

    
    def generate_world(self):
        """
        Randomly select a world type and exactly 5 features.
        """
        world_types = [
            "Fantasy Kingdom", "Dark Fantasy", "Sci-Fi Galaxy", "Post-Apocalyptic",
            "Medieval Realm", "Cyberpunk City", "Steampunk World",
            "Mythological Realm", "Magical Academy", "Horror Realm"
        ]

        features = [
            "Magic System", "Advanced Technology", "Ancient Ruins",
            "Hidden Treasures", "Dangerous Creatures", "Political Conflict",
            "Guilds & Factions", "Mystical Artifacts", "Harsh Environment",
            "Time Travel"
        ]

        random_type = random.choice(world_types)
        random_features = random.sample(features, 5)

        self.world_type.set(random_type)

        for feature, var in self.feature_vars.items():
            if feature in random_features:
                var.set(True)
            else:
                var.set(False)

        self.mark_unsaved()


    def save_world(self):
        """
        Validate and save world information.
        """
        name = self.name.get().strip()
        selected_type = self.world_type.get()
        selected_features = self.get_selected_features()

        if name == "":
            self.controller.show_error_popup("Please enter a world name.", "World Error")
            return

        if selected_type == "NONE":
            self.controller.show_error_popup("Please choose a world type.", "World Error")
            return

        if len(selected_features) != 5:
            self.controller.show_error_popup("Please select exactly 5 features.", "World Error")
            return

        self.controller.world = {
            "name": name,
            "type": selected_type,
            "features": selected_features,
            "character": self.controller.character
        }

        username = self.controller.current_user

        # Make sure user exists
        if username not in self.controller.saved_worlds:
            self.controller.saved_worlds[username] = {}

        if self.controller.current_world_name is None:
            self.controller.current_world_name = name

        # Save/update world with username
        self.controller.saved_worlds[username][self.controller.current_world_name] = self.controller.world
        self.controller.save_worlds()

        self.unsaved_changes = False

        self.controller.show_error_popup("World saved successfully!", "World Saved")