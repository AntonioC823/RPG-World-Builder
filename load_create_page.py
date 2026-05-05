import tkinter as tk

class LoadCreatePage(tk.Frame):
    """
    Load/Create RPG page.
    """

    def __init__(self, parent, controller):
        """
        Initialize Load/Create RPG page widgets.
        """
        super().__init__(parent, bg="#f4f4f4")
        self.controller = controller

        # Main centered page frame
        page_frame = tk.Frame(self, bg="#f4f4f4")
        page_frame.place(relx=0.5, rely=0.5, anchor="center", width=520, height=600)

        # Page heading above the box
        tk.Label(
            self,
            text="Load/Create\nRPG",
            font=("Arial", 24),
            bg="#f4f4f4"
        ).place(relx=0.5, rely=0.20, anchor="center")

        # Search RPG Worlds label
        tk.Label(
            page_frame,
            text="Search RPG Worlds",
            font=("Arial", 14),
            bg="#f4f4f4"
        ).place(relx=0.28, rely=0.33, anchor="center")

        # Search input box
        self.search_entry = tk.Entry(
            page_frame,
            width=28,
            font=("Arial", 12)
        )
        self.search_entry.place(relx=0.255, rely=0.39, anchor="center", width=220, height=35)

        # Update list only when user types
        self.search_entry.bind("<KeyRelease>", self.update_world_list)

        # Dropdown arrow button
        tk.Button(
            page_frame,
            text="▼",
            font=("Arial", 10),
            command=self.show_all_worlds
        ).place(relx=0.485, rely=0.39, anchor="center", width=30, height=35)

        # Saved worlds listbox, hidden at first
        self.world_listbox = tk.Listbox(
            page_frame,
            font=("Arial", 12),
            height=5
        )

        # click a world to autofill in search bar
        self.world_listbox.bind("<ButtonRelease-1>", self.select_world_name)

        # Hide the dropdown list if user clicks anywhere else
        self.controller.root.bind("<Button-1>", self.hide_dropdown)

        # Load selected world button
        tk.Button(
            page_frame,
            text="Load Selected World",
            font=("Arial", 12),
            command=self.load_selected_world
        ).place(relx=0.28, rely=0.460, anchor="center", width=180, height=35)

        # Create new RPG button
        tk.Button(
            page_frame,
            text="Create new\nRPG",
            font=("Arial", 14),
            command=self.create_new_rpg
        ).place(relx=0.75, rely=0.38, anchor="center", width=190, height=95)

        # Recent builds label
        tk.Label(
            page_frame,
            text="Recent RPG Builds:",
            font=("Arial", 14),
            bg="#f4f4f4",
        ).place(relx=0.5, rely=0.55, anchor="center", width=230, height=40)

        # RPG 1 button
        self.recent_button_1 = tk.Button(
            page_frame,
            text="No recent world",
            font=("Arial", 16),
            command=lambda: self.load_recent_world(0)
        )
        self.recent_button_1.place(relx=0.30, rely=0.70, anchor="center", width=190, height=95)

        # RPG 2 button
        self.recent_button_2 = tk.Button(
            page_frame,
            text="No recent world",
            font=("Arial", 16),
            command=lambda: self.load_recent_world(1)
        )
        self.recent_button_2.place(relx=0.70, rely=0.70, anchor="center", width=190, height=95)

        # Logout button
        tk.Button(
            page_frame,
            text="Logout Button",
            font=("Arial", 16),
            command=self.logout_with_warning
        ).place(relx=0.23, rely=0.93, anchor="center", width=230, height=45)

        # Help button
        tk.Button(
            page_frame,
            text="Help Button",
            font=("Arial", 16),
            command=lambda: controller.show_page("HelpPage")
        ).place(relx=0.77, rely=0.93, anchor="center", width=230, height=45)

    
    def search_rpg(self):
        """
        Search for an RPG world using the entered world name.
        """
        world_name = self.search_entry.get().strip()

        if world_name == "":
            self.controller.show_error_popup("Please enter a world name to search.", "Search Error")
            return

        current_user = self.controller.current_user

        if current_user in self.controller.saved_worlds:
            user_worlds = self.controller.saved_worlds[current_user]

            for saved_name, saved_world in user_worlds.items():
                if saved_name.lower() == world_name.lower():
                    self.show_launch_world_popup(saved_world)
                    return

        self.controller.show_error_popup(f"No saved world found named {world_name}.", "Search Error")

    
    def update_world_list(self, event=None):
        """
        Filter the saved worlds list as the user types.
        """
        self.world_listbox.delete(0, tk.END)

        username = self.controller.current_user
        search_text = self.search_entry.get().strip().lower()

        if search_text == "":
            self.world_listbox.place_forget()
            return

        user_worlds = self.controller.saved_worlds.get(username, {})

        matching_worlds = []
        for world_name in user_worlds:
            if search_text in world_name.lower():
                matching_worlds.append(world_name)

        matching_worlds.sort()

        if not matching_worlds:
            self.world_listbox.place_forget()
            return

        for world_name in matching_worlds:
            self.world_listbox.insert(tk.END, world_name)

        self.world_listbox.place_forget()
        self.world_listbox.place(relx=0.28, rely=0.42, anchor="n", width=250, height=min(len(matching_worlds), 5) * 22)
        self.world_listbox.lift()

    
    def show_all_worlds(self):
        """
        Show all saved worlds in alphabetical order.
        """
        self.world_listbox.delete(0, tk.END)

        username = self.controller.current_user
        user_worlds = self.controller.saved_worlds.get(username, {})

        world_names = list(user_worlds.keys())
        world_names.sort()

        if not world_names:
            self.controller.show_error_popup("No saved worlds found.", "Saved Worlds")
            return

        for world_name in world_names:
            self.world_listbox.insert(tk.END, world_name)

        self.world_listbox.place_forget()
        self.world_listbox.place(relx=0.28, rely=0.42, anchor="n", width=250, height=min(len(world_names), 5) * 22)
        self.world_listbox.lift()

    def hide_dropdown(self, event):
        widget = event.widget

        if widget == self.search_entry or widget == self.world_listbox:
            return

        if self.world_listbox.winfo_ismapped():
            self.world_listbox.place_forget()

    
    def select_world_name(self, event=None):
        """
        Autofill the search box with the selected world name and hide the dropdown.
        """
        selected_index = self.world_listbox.curselection()

        if not selected_index:
            return

        selected_world_name = self.world_listbox.get(selected_index[0])

        self.search_entry.delete(0, tk.END)
        self.search_entry.insert(0, selected_world_name)

        self.world_listbox.place_forget()


    def load_selected_world(self):
        """
        Load the world selected from the search box.
        """
        selected_world_name = self.search_entry.get().strip()
        username = self.controller.current_user

        if selected_world_name == "":
            self.controller.show_error_popup("Please select or enter a world name.", "Load World Error")
            return

        if username not in self.controller.saved_worlds:
            self.controller.show_error_popup("No saved worlds for this user.", "Load World Error")
            return

        if selected_world_name not in self.controller.saved_worlds[username]:
            self.controller.show_error_popup("Selected world not found.", "Load World Error")
            return

        saved_world = self.controller.saved_worlds[username][selected_world_name]

        self.show_launch_world_popup(saved_world)

    
    def show_launch_world_popup(self, saved_world):
        """
        Ask the user if they want to launch the found world.
        """
        popup = tk.Toplevel(self.controller.root)
        popup.title("Confirm Launch")
        popup.geometry("420x180")
        popup.resizable(False, False)

        self.controller.root.update_idletasks()
        x = self.controller.root.winfo_x() + (self.controller.root.winfo_width() // 2) - 210
        y = self.controller.root.winfo_y() + (self.controller.root.winfo_height() // 2) - 90
        popup.geometry(f"420x180+{x}+{y}")

        tk.Label(
            popup,
            text=f"Are you sure you want to launch\nWorld '{saved_world['name']}'?",
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
            command=lambda: self.launch_world(saved_world, popup)
        ).pack(side="left", padx=10)

        tk.Button(
            button_frame,
            text="No",
            width=10,
            command=popup.destroy
        ).pack(side="left", padx=10)

        popup.transient(self.controller.root)
        popup.grab_set()

    
    def launch_world(self, saved_world, popup):
        """
        Load the selected world and go to the View World page.
        """
        self.controller.world = saved_world
        self.controller.current_world_name = saved_world["name"]

        if "character" in saved_world:
            self.controller.character = saved_world["character"]

        popup.destroy()
        self.controller.show_page("ViewWorldPage")

    
    def create_new_rpg(self):
        """
        Start a new RPG build for the current user.
        """
        self.controller.current_world_name = None
        self.controller.character = {}
        self.controller.world = {}

        self.controller.show_page("CharacterPage")

    def update_recent_worlds(self):
        """
        Display the two most recent worlds for the current user.
        """
        username = self.controller.current_user
        user_worlds = self.controller.saved_worlds.get(username, {})

        recent_worlds = list(user_worlds.items())[-2:]
        recent_worlds.reverse()

        buttons = [self.recent_button_1, self.recent_button_2]

        for index, button in enumerate(buttons):
            if index < len(recent_worlds):
                world_name, world_data = recent_worlds[index]
                character = world_data.get("character", {})
                character_name = character.get("name", "No character")

                button.config(
                    text=f"World: {world_name}\nCharacter: {character_name}",
                    state="normal"
                )
            else:
                button.config(
                    text="No recent world",
                    state="disabled"
                )


    def load_recent_world(self, index):
        """
        Load one of the recent worlds.
        """
        username = self.controller.current_user
        user_worlds = self.controller.saved_worlds.get(username, {})

        recent_worlds = list(user_worlds.items())[-2:]
        recent_worlds.reverse()

        if index >= len(recent_worlds):
            return

        world_name, saved_world = recent_worlds[index]
        self.search_entry.delete(0, tk.END)
        self.search_entry.insert(0, world_name)
        self.show_launch_world_popup(saved_world)

    def logout_with_warning(self):
        """
        Ask the user to confirm logout.
        """
        popup = tk.Toplevel(self.controller.root)
        popup.title("Confirm Logout")
        popup.geometry("420x180")
        popup.resizable(False, False)

        # Center popup
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