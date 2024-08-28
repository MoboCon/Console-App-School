from tkinter import ttk, messagebox
import tkinter as tk  # Importă tkinter corect

class LoginWindow:
    def __init__(self, root, auth_system, on_login_success):
        self.root = root
        self.auth_system = auth_system
        self.on_login_success = on_login_success

        self.root.title("Login")
        self.root.geometry("400x300")
        self.root.configure(bg="#2C3E50")

        self.title_label = ttk.Label(root, text="Login to Gradebook", font=("Helvetica", 16, "bold"), background="#2C3E50", foreground="white")
        self.title_label.pack(pady=20)

        self.username_label = ttk.Label(root, text="Username", background="#2C3E50", foreground="white")
        self.username_label.pack(pady=5)
        self.username_entry = ttk.Entry(root)
        self.username_entry.pack(pady=5)

        self.password_label = ttk.Label(root, text="Password", background="#2C3E50", foreground="white")
        self.password_label.pack(pady=5)
        self.password_entry = ttk.Entry(root, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = ttk.Button(root, text="Login", command=self.login)
        self.login_button.pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.auth_system.authenticate(username, password):
            self.on_login_success()
            self.root.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
