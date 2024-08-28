from tkinter import Tk
from tkinterdnd2 import TkinterDnD
from auth_system import AuthSystem
from GradebookApp import GradebookApp
from login_window import LoginWindow

def main():
    auth_system = AuthSystem()
    login_root = Tk()
    app = LoginWindow(login_root, auth_system, lambda: run_main_app(auth_system))
    login_root.mainloop()

def run_main_app(auth_system):
    root = TkinterDnD.Tk()
    app = GradebookApp(root, auth_system)
    root.mainloop()

if __name__ == "__main__":
    main()
