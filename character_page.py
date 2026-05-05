import tkinter as tk
import random

class CharacterPage(tk.Frame):
    """
    Create/Edit Character page. Allows users to enter a character name, choose one class, choose up to three attributes, and save the character.
    """

    def __init__(self, parent, controller):
        """
        Initialize character page widgets.
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
            text="Generate/Edit World",
            font=("Arial", 11),
            command=lambda: self.navigate_with_warning("WorldPage")
        ).pack(side="left", padx=10, pady=8)

        tk.Button(
            nav_frame,
            text="View World",
            font=("Arial", 11),
            command=lambda: self.navigate_with_warning("ViewWorldPage")
        ).pack(side="left", padx=10, pady=8)

        container = tk.Frame(self, bg="#f4f4f4")
        container.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            container,
            text="Create/Edit Character",
            font=("Arial", 32),
            bg="#f4f4f4"
        ).pack(pady=15)

        tk.Label(
            container,
            text="Enter character details below.",
            font=("Arial", 14),
            bg="#f4f4f4"
        ).pack(pady=5)

        tk.Label(container, text="Character Name", font=("Arial", 14), bg="#f4f4f4").pack(pady=5)
        self.name = tk.Entry(container, width=35, font=("Arial", 12))
        self.name.pack(pady=5)

        self.name.bind("<KeyRelease>", self.mark_unsaved)

        # Character class selection
        tk.Label(container, text="Choose a Character Class", font=("Arial", 14), bg="#f4f4f4").pack(pady=10)

        self.character_class = tk.StringVar()
        self.character_class.set("NONE")

        class_frame = tk.Frame(container, bg="#f4f4f4")
        class_frame.pack(pady=5)

        for class_name in ["Warrior", "Mage", "Rogue"]:
            tk.Radiobutton(
                class_frame,
                text=class_name,
                variable=self.character_class,
                value=class_name,
                font=("Arial", 12),
                bg="#f4f4f4",
                command=self.mark_unsaved
            ).pack(side="left", padx=15)

        # Attribute selection
        tk.Label(
            container,
            text="Choose 3 Character Attributes",
            font=("Arial", 14),
            bg="#f4f4f4"
        ).pack(pady=10)

        self.attribute_vars = {}

        attributes = [
            "Strength", "Intelligence", "Agility", "Endurance", "Charisma",
            "Luck", "Dexterity", "Wisdom", "Perception", "Vitality"
        ]

        attribute_frame = tk.Frame(container, bg="#f4f4f4")
        attribute_frame.pack(pady=5)

        for index, attribute in enumerate(attributes):
            var = tk.BooleanVar()
            self.attribute_vars[attribute] = var

            checkbox = tk.Checkbutton(
                attribute_frame,
                text=attribute,
                variable=var,
                font=("Arial", 11),
                bg="#f4f4f4",
                command=self.attribute_changed
            )

            checkbox.grid(row=index // 5, column=index % 5, sticky="w", padx=10, pady=5)

        tk.Button(
            container,
            text="Generate Character",
            width=25,
            font=("Arial", 12),
            command=self.generate_character
        ).pack(pady=10)

        tk.Button(
            container,
            text="Save Character",
            width=25,
            font=("Arial", 12),
            command=self.save_character
        ).pack(pady=15)

        tk.Button(
            container,
            text="Logout",
            width=25,
            font=("Arial", 12),
            command=self.logout_with_warning
        ).pack(pady=5)

        tk.Button(
            container,
            text="Help",
            width=25,
            font=("Arial", 12),
            command=lambda: self.navigate_with_warning("HelpPage")
        ).pack(pady=5)

    def get_selected_attributes(self):
        """
        Return a list of selected character attributes.
        """
        selected_attributes = []

        for attribute, var in self.attribute_vars.items():
            if var.get():
                selected_attributes.append(attribute)

        return selected_attributes

    def limit_attributes(self):
        """
        Prevent users from selecting more than three attributes.
        """
        selected_attributes = self.get_selected_attributes()

        if len(selected_attributes) > 3:
            self.controller.show_error_popup(
                "You can only choose up to 3 attributes.",
                "Attribute Selection Error"
            )

            # Uncheck the most recently selected attribute.
            for attribute, var in self.attribute_vars.items():
                if var.get() and attribute == selected_attributes[-1]:
                    var.set(False)
                    break

    def mark_unsaved(self, event=None):
        """
        Mark the character page as having unsaved changes.
        """
        self.unsaved_changes = True


    def attribute_changed(self):
        """
        Mark changes and enforce the attribute limit.
        """
        self.mark_unsaved()
        self.limit_attributes()


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

    def generate_character(self):
        """
        Randomly select a character class and exactly 3 attributes.
        """
        classes = ["Warrior", "Mage", "Rogue"]

        attributes = [
            "Strength", "Intelligence", "Agility", "Endurance", "Charisma",
            "Luck", "Dexterity", "Wisdom", "Perception", "Vitality"
        ]

        random_class = random.choice(classes)
        random_attributes = random.sample(attributes, 3)

        self.character_class.set(random_class)

        for attribute, var in self.attribute_vars.items():
            if attribute in random_attributes:
                var.set(True)
            else:
                var.set(False)

        self.mark_unsaved()

    def save_character(self):
        """
        Validate and save character information.
        """
        name = self.name.get().strip()
        selected_class = self.character_class.get()
        selected_attributes = self.get_selected_attributes()

        if name == "":
            self.controller.show_error_popup(
                "Please enter a character name.",
                "Character Error"
            )
            return

        if selected_class == "NONE":
            self.controller.show_error_popup(
                "Please choose a character class.",
                "Character Error"
            )
            return

        if len(selected_attributes) != 3:
            self.controller.show_error_popup(
                "Please choose exactly 3 character attributes.",
                "Character Error"
            )
            return

        self.controller.character = {
            "name": name,
            "class": selected_class,
            "attributes": selected_attributes
        }

        self.unsaved_changes = False

        self.controller.show_error_popup(
            "Character saved successfully!",
            "Character Saved"
        )