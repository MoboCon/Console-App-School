class ThemeManager:
    def __init__(self, root):
        self.root = root
        self.themes = {
            "Light": {"bg": "#f0f0f0", "fg": "#000000"},
            "Dark": {"bg": "#333333", "fg": "#ffffff"}
        }
        self.current_theme = "Light"

    def apply_theme(self, theme_name):
        if theme_name in self.themes:
            theme = self.themes[theme_name]
            self.root.configure(bg=theme["bg"])
            for widget in self.root.winfo_children():
                widget.configure(bg=theme["bg"], fg=theme["fg"])
