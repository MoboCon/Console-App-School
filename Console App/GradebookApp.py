import tkinter as tk
from tkinter import ttk, messagebox
from tkinterdnd2 import TkinterDnD
from gradebook import Gradebook
import tkcalendar as tkc
import ttkbootstrap as tb

class GradebookApp:
    def __init__(self, root, auth_system):
        self.gradebook = Gradebook()
        self.root = root
        self.auth_system = auth_system
        self.root.title("Teacher's Dashboard")
        self.root.geometry("1200x800")

        # Aplicăm tema modernă cu accent pe culoarea verde
        self.style = tb.Style("flatly")
        self.style.configure('TLabel', background='#E8F6EF', foreground='#1B5E20')
        self.style.configure('TButton', background='#1B5E20', foreground='white')
        self.style.configure('TFrame', background='#E8F6EF')

        # Dashboard principal
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # Crearea interfeței principale
        self.create_main_interface()

    def create_main_interface(self):
        # Titlul aplicației
        self.title_label = ttk.Label(self.main_frame, text="Teacher's Dashboard", font=("Helvetica", 24, "bold"))
        self.title_label.pack(pady=20)

        # Panou de control
        control_frame = ttk.Frame(self.main_frame)
        control_frame.pack(pady=20)

        self.add_student_button = ttk.Button(control_frame, text="Add Student", command=self.open_add_student_dialog)
        self.add_student_button.grid(row=0, column=0, padx=10)

        self.add_course_button = ttk.Button(control_frame, text="Add Course", command=self.open_add_course_dialog)
        self.add_course_button.grid(row=0, column=1, padx=10)

        self.add_grade_button = ttk.Button(control_frame, text="Add Grade", command=self.open_add_grade_dialog)
        self.add_grade_button.grid(row=0, column=2, padx=10)

        self.view_attendance_button = ttk.Button(control_frame, text="View Attendance", command=self.open_view_attendance_dialog)
        self.view_attendance_button.grid(row=0, column=3, padx=10)

        self.view_grades_button = ttk.Button(control_frame, text="View Grades", command=self.open_view_grades_dialog)
        self.view_grades_button.grid(row=0, column=4, padx=10)

        self.manage_attendance_button = ttk.Button(control_frame, text="Manage Attendance", command=self.open_manage_attendance_dialog)
        self.manage_attendance_button.grid(row=0, column=5, padx=10)

        # Listă elevi și cursuri
        list_frame = ttk.Frame(self.main_frame)
        list_frame.pack(fill="both", expand=True, pady=20)

        self.student_listbox = tk.Listbox(list_frame, selectmode=tk.SINGLE, width=40, height=20, bg="#E8F6EF", fg="#1B5E20", font=("Helvetica", 12))
        self.student_listbox.pack(side="left", padx=10, pady=10)

        self.course_listbox = tk.Listbox(list_frame, selectmode=tk.SINGLE, width=40, height=20, bg="#E8F6EF", fg="#1B5E20", font=("Helvetica", 12))
        self.course_listbox.pack(side="left", padx=10, pady=10)

        self.refresh_student_listbox()

        self.student_listbox.bind('<<ListboxSelect>>', self.on_student_select)

    def refresh_student_listbox(self):
        self.student_listbox.delete(0, tk.END)
        for student_name in self.gradebook.list_students():
            self.student_listbox.insert(tk.END, student_name)

    def refresh_course_listbox(self, student_name):
        self.course_listbox.delete(0, tk.END)
        student = self.gradebook.find_student(student_name)
        if student:
            for course_name in student.get_courses().keys():
                self.course_listbox.insert(tk.END, course_name)

    def on_student_select(self, event):
        selected_student = self.get_selected_student()
        if selected_student:
            self.refresh_course_listbox(selected_student)

    def get_selected_student(self):
        try:
            return self.student_listbox.get(self.student_listbox.curselection()[0])
        except IndexError:
            return None

    def open_add_student_dialog(self):
        AddStudentDialog(self.root, self.gradebook, self.refresh_student_listbox)

    def open_add_course_dialog(self):
        selected_student = self.get_selected_student()
        if selected_student:
            AddCourseDialog(self.root, self.gradebook, selected_student, lambda: self.refresh_course_listbox(selected_student))
        else:
            messagebox.showwarning("Selection Error", "Please select a student first.")

    def open_add_grade_dialog(self):
        selected_student = self.get_selected_student()
        if selected_student:
            AddGradeDialog(self.root, self.gradebook, selected_student)
        else:
            messagebox.showwarning("Selection Error", "Please select a student first.")

    def open_view_attendance_dialog(self):
        selected_student = self.get_selected_student()
        if selected_student:
            ViewAttendanceDialog(self.root, self.gradebook, selected_student)
        else:
            messagebox.showwarning("Selection Error", "Please select a student first.")

    def open_view_grades_dialog(self):
        selected_student = self.get_selected_student()
        if selected_student:
            ViewGradesDialog(self.root, self.gradebook, selected_student)
        else:
            messagebox.showwarning("Selection Error", "Please select a student first.")

    def open_manage_attendance_dialog(self):
        selected_student = self.get_selected_student()
        if selected_student:
            ManageAttendanceDialog(self.root, self.gradebook, selected_student)
        else:
            messagebox.showwarning("Selection Error", "Please select a student first.")

# Dialoguri pentru adăugarea de elevi, cursuri și note, vizualizarea notelor și gestionarea prezenței

class AddStudentDialog:
    def __init__(self, parent, gradebook, refresh_callback):
        self.gradebook = gradebook
        self.refresh_callback = refresh_callback
        self.top = tk.Toplevel(parent)
        self.top.title("Add Student")
        self.top.geometry("400x200")

        self.label = ttk.Label(self.top, text="Student Name:")
        self.label.pack(pady=20)

        self.entry = ttk.Entry(self.top)
        self.entry.pack(pady=10)

        self.submit_button = ttk.Button(self.top, text="Add", command=self.submit)
        self.submit_button.pack(pady=10)

    def submit(self):
        student_name = self.entry.get()
        if student_name:
            try:
                self.gradebook.add_student(student_name)
                self.refresh_callback()
                self.top.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

class AddCourseDialog:
    def __init__(self, parent, gradebook, student_name, refresh_callback):
        self.gradebook = gradebook
        self.student_name = student_name
        self.refresh_callback = refresh_callback
        self.top = tk.Toplevel(parent)
        self.top.title("Add Course")
        self.top.geometry("400x200")

        self.label = ttk.Label(self.top, text="Course Name:")
        self.label.pack(pady=20)

        self.entry = ttk.Entry(self.top)
        self.entry.pack(pady=10)

        self.submit_button = ttk.Button(self.top, text="Add", command=self.submit)
        self.submit_button.pack(pady=10)

    def submit(self):
        course_name = self.entry.get()
        if course_name:
            try:
                self.gradebook.add_course_to_student(self.student_name, course_name)
                self.refresh_callback()
                self.top.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

class AddGradeDialog:
    def __init__(self, parent, gradebook, student_name):
        self.gradebook = gradebook
        self.student_name = student_name
        self.top = tk.Toplevel(parent)
        self.top.title("Add Grade")
        self.top.geometry("400x300")

        self.label = ttk.Label(self.top, text="Select Course:")
        self.label.pack(pady=20)

        self.course_combobox = ttk.Combobox(self.top, state="readonly")
        self.course_combobox.pack(pady=10)
        self.course_combobox['values'] = list(self.gradebook.find_student(student_name).get_courses().keys())

        self.grade_label = ttk.Label(self.top, text="Enter Grade:")
        self.grade_label.pack(pady=20)

        self.grade_entry = ttk.Entry(self.top)
        self.grade_entry.pack(pady=10)

        self.submit_button = ttk.Button(self.top, text="Add", command=self.submit)
        self.submit_button.pack(pady=10)

    def submit(self):
        course_name = self.course_combobox.get()
        grade = self.grade_entry.get()
        if course_name and grade:
            try:
                self.gradebook.record_grade(self.student_name, course_name, float(grade))
                self.top.destroy()
                messagebox.showinfo("Success", f"Added grade {grade} for {course_name}.")
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid grade.")
        else:
            messagebox.showwarning("Input Error", "Please select a course and enter a grade.")

class ViewAttendanceDialog:
    def __init__(self, parent, gradebook, student_name):
        self.gradebook = gradebook
        self.student_name = student_name
        self.top = tk.Toplevel(parent)
        self.top.title("View Attendance")
        self.top.geometry("500x400")

        self.attendance_listbox = tk.Listbox(self.top, selectmode=tk.SINGLE, width=50, height=20, bg="#E8F6EF", fg="#1B5E20", font=("Helvetica", 12))
        self.attendance_listbox.pack(pady=20)

        student = self.gradebook.find_student(student_name)
        if student:
            for date, status in student.get_attendance().items():
                status_text = "Present" if status else "Absent"
                self.attendance_listbox.insert(tk.END, f"{date}: {status_text}")

class ViewGradesDialog:
    def __init__(self, parent, gradebook, student_name):
        self.gradebook = gradebook
        self.student_name = student_name
        self.top = tk.Toplevel(parent)
        self.top.title("View Grades")
        self.top.geometry("500x400")

        self.grades_listbox = tk.Listbox(self.top, selectmode=tk.SINGLE, width=50, height=20, bg="#E8F6EF", fg="#1B5E20", font=("Helvetica", 12))
        self.grades_listbox.pack(pady=20)

        student = self.gradebook.find_student(student_name)
        if student:
            for course_name, grades in student.get_courses().items():
                grades_text = ", ".join(map(str, grades))
                self.grades_listbox.insert(tk.END, f"{course_name}: {grades_text}")

class ManageAttendanceDialog:
    def __init__(self, parent, gradebook, student_name):
        self.gradebook = gradebook
        self.student_name = student_name
        self.top = tk.Toplevel(parent)
        self.top.title("Manage Attendance")
        self.top.geometry("500x500")

        self.calendar = tkc.Calendar(self.top, selectmode="day", date_pattern="y-mm-dd", showweeknumbers=False, background="#E8F6EF", foreground="#1B5E20")
        self.calendar.pack(pady=20)

        self.mark_present_button = ttk.Button(self.top, text="Mark Present", command=self.mark_present)
        self.mark_present_button.pack(side="left", padx=20, pady=10)

        self.mark_absent_button = ttk.Button(self.top, text="Mark Absent", command=self.mark_absent)
        self.mark_absent_button.pack(side="right", padx=20, pady=10)

    def mark_present(self):
        date = self.calendar.get_date()
        self.gradebook.mark_attendance(self.student_name, date, True)
        messagebox.showinfo("Success", f"Marked {self.student_name} present on {date}.")

    def mark_absent(self):
        date = self.calendar.get_date()
        self.gradebook.mark_attendance(self.student_name, date, False)
        messagebox.showinfo("Success", f"Marked {self.student_name} absent on {date}.")
