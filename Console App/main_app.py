import tkinter as tk  # Importă tkinter corect
from tkinter import ttk, simpledialog, messagebox, filedialog
from tkinterdnd2 import TkinterDnD
from gradebook import Gradebook  # Importă clasa Gradebook
from notification_system import NotificationSystem  # Importă NotificationSystem
from theme_manager import ThemeManager  # Importă ThemeManager
import tkcalendar as tkc  # Importă calendarul
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Restul codului pentru aplicația ta...


class GradebookApp:
    def __init__(self, root, auth_system):
        self.gradebook = Gradebook()
        self.root = root
        self.auth_system = auth_system
        self.root.title("Advanced Gradebook")
        self.root.geometry("1000x700")
        self.notification_system = NotificationSystem()
        self.theme_manager = ThemeManager(root)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        self.create_teacher_interface()  # Creăm interfața pentru profesori

    def create_teacher_interface(self):
        teacher_tab = ttk.Frame(self.notebook)
        self.notebook.add(teacher_tab, text="Teacher's Dashboard")

        # Secțiune pentru selectarea elevilor
        self.student_listbox = tk.Listbox(teacher_tab, selectmode=tk.SINGLE, width=40, height=10)
        self.student_listbox.grid(row=0, column=0, padx=10, pady=10)
        
        self.refresh_student_listbox()

        # Secțiune pentru gestionarea materiilor și notelor
        self.course_entry = ttk.Entry(teacher_tab, width=40)
        self.course_entry.grid(row=1, column=0, padx=10, pady=10)
        self.add_course_button = ttk.Button(teacher_tab, text="Add Course", command=self.add_course)
        self.add_course_button.grid(row=1, column=1, padx=10, pady=10)

        self.grade_entry = ttk.Entry(teacher_tab, width=40)
        self.grade_entry.grid(row=2, column=0, padx=10, pady=10)
        self.add_grade_button = ttk.Button(teacher_tab, text="Add Grade", command=self.add_grade)
        self.add_grade_button.grid(row=2, column=1, padx=10, pady=10)

        # Secțiune pentru gestionarea absențelor cu calendar
        self.calendar = self.create_calendar(teacher_tab)
        self.calendar.grid(row=3, column=0, padx=10, pady=10, columnspan=2)

        self.mark_absent_button = ttk.Button(teacher_tab, text="Mark Absent", command=self.mark_absent)
        self.mark_absent_button.grid(row=4, column=0, padx=10, pady=10, columnspan=2)

    def refresh_student_listbox(self):
        self.student_listbox.delete(0, tk.END)
        for student_name in self.gradebook.list_students():
            self.student_listbox.insert(tk.END, student_name)
    
    def add_course(self):
        selected_student = self.get_selected_student()
        if selected_student:
            course_name = self.course_entry.get()
            if course_name:
                self.gradebook.add_course_to_student(selected_student, course_name)
                messagebox.showinfo("Success", f"Added course '{course_name}' to {selected_student}.")
            else:
                messagebox.showwarning("Input Error", "Please enter a course name.")
    
    def add_grade(self):
        selected_student = self.get_selected_student()
        if selected_student:
            course_name = self.course_entry.get()
            grade = self.grade_entry.get()
            if course_name and grade:
                try:
                    self.gradebook.record_grade(selected_student, course_name, float(grade))
                    messagebox.showinfo("Success", f"Added grade {grade} for {course_name}.")
                except ValueError:
                    messagebox.showerror("Input Error", "Please enter a valid number for the grade.")
            else:
                messagebox.showwarning("Input Error", "Please enter both course name and grade.")
    
    def mark_absent(self):
        selected_student = self.get_selected_student()
        if selected_student:
            date = self.calendar.get_date()
            self.gradebook.mark_attendance(selected_student, date, False)
            messagebox.showinfo("Success", f"Marked {selected_student} absent on {date}.")
    
    def get_selected_student(self):
        try:
            return self.student_listbox.get(self.student_listbox.curselection()[0])
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a student first.")
            return None

    def create_calendar(self, parent):
        return tkc.Calendar(parent, selectmode="day", date_pattern="y-mm-dd")
