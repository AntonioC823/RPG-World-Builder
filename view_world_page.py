import tkinter as tk
from microservices import request_prompt, request_statistics

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

        self.output = tk.Text(container, width=90, height=20, font=("Arial", 12), wrap="word")
        self.output.pack(pady=10)

        tk.Button(
            container,
            text="Generate Story",
            width=25,
            font=("Arial", 12),
            command=self.generate_story
        ).pack(pady=6)

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

        self.output.config(state="normal")
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

            genre = world.get("genre", "Unknown")
            theme = world.get("theme", "Unknown")
            story = world.get("story", "Story unavailable.")

            self.output.insert(tk.END, "\n--- Story ---\n\n")
            self.output.insert(tk.END, f"Genre: {genre}\n")
            self.output.insert(tk.END, f"Theme: {theme}\n\n")
            self.output.insert(tk.END, f"{story}\n")
        else:
            self.output.insert(tk.END, "No world saved yet.\n")

        self.output.config(state="disabled")


    def generate_story(self):
        """
        Generate a story for the currently loaded world.
        """
        world = self.controller.world
        character = self.controller.character

        request_details = {
            "world_name": world.get("name"),
            "world_type": world.get("type"),
            "world_features": world.get("features"),
            "character": character
        }

        story = request_prompt(
            "Generate a short RPG story for this character and world. "
            "Write in plain text only. "
            "Do not use markdown formatting, asterisks, bold text, bullet points, or headings.",
            request_details
        ) or "Story unavailable."

        world["story"] = story

        username = self.controller.current_user
        world_name = self.controller.current_world_name

        self.controller.saved_worlds[username][world_name] = world

        request_statistics({
            "event": {
                "app_name": "RPG Worldbuilder",
                "user_id": username,
                "event_type": "story_generated"
            }
        })

        if "_stats" not in self.controller.saved_worlds[username]:
            self.controller.saved_worlds[username]["_stats"] = {
                "world_created": 0,
                "character_created": 0,
                "story_generated": 0
            }

        self.controller.saved_worlds[username]["_stats"]["story_generated"] += 1
        
        self.controller.save_worlds()

        self.refresh_view()


    def logout_with_warning(self):
        """
        Ask the user to confirm logout.
        """
        self.controller.show_confirm_popup(
            "Are you sure you want to logout?",
            "Confirm Logout",
            self.controller.logout
        )