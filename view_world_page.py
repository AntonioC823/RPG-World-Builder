import tkinter as tk

class ViewWorldPage(tk.Frame):
    """
    View World page.
    """

    def __init__(self, parent, controller):
        """
        Initialize view world page widgets.
        """
        super().__init__(parent, bg="#f4f4f4")
        self.controller = controller

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

        container = tk.Frame(self, bg="#f4f4f4")
        container.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            container,
            text="View World",
            font=("Arial", 32),
            bg="#f4f4f4"
        ).pack(pady=20)

        self.output = tk.Text(container, width=90, height=20, font=("Arial", 12))
        self.output.pack(pady=10)

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
            command=lambda: controller.show_page("HelpPage")
        ).pack(pady=6)

    def refresh_view(self):
        """
        Display saved character and world information.
        """
        self.output.delete("1.0", tk.END)

        character = self.controller.character
        world = self.controller.world

        self.output.insert(tk.END, "\n--- Character ---\n\n")
        if "name" in character and "class" in character and "attributes" in character:
            self.output.insert(tk.END, f"Name: {character['name']}\n")
            self.output.insert(tk.END, f"Class: {character['class']}\n")
            self.output.insert(tk.END, f"Attributes: {', '.join(character['attributes'])}\n\n")
        else:
            self.output.insert(tk.END, "No character saved yet.\n")

        self.output.insert(tk.END, "\n--- World ---\n\n")
        if "name" in world and "type" in world and "features" in world:
            self.output.insert(tk.END, f"World Name: {world['name']}\n")
            self.output.insert(tk.END, f"World Type: {world['type']}\n")

            features_str = ", ".join(world["features"])
            self.output.insert(tk.END, f"World Features: {features_str}\n\n")

            self.output.insert(
                tk.END,
                f"\nStory: {world['name']} is a {world['type']} world shaped by {features_str}.\n"
            )
        else:
            self.output.insert(tk.END, "No world saved yet.\n")


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