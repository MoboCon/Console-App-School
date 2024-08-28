class Course:
    def __init__(self, name):
        self.name = name
        self.grades = []

    def add_grade(self, grade):
        self.grades.append(grade)

    def get_average(self):
        if self.grades:
            return sum(self.grades) / len(self.grades)
        return 0

class Student:
    def __init__(self, name):
        self.name = name
        self.courses = {}
        self.attendance = {}

    def add_course(self, name):
        if name not in self.courses:
            self.courses[name] = Course(name)

    def add_grade(self, course_name, grade):
        if course_name in self.courses:
            self.courses[course_name].add_grade(grade)
        else:
            raise ValueError("Course not found")

    def mark_attendance(self, date, present):
        self.attendance[date] = present

    def get_courses(self):
        return self.courses

    def get_attendance(self):
        return self.attendance

    def get_average(self, course_name):
        if course_name in self.courses:
            return self.courses[course_name].get_average()
        return 0

class Gradebook:
    def __init__(self):
        self.students = {}

    def add_student(self, name):
        if name in self.students:
            raise ValueError("Student already exists")
        self.students[name] = Student(name)

    def remove_student(self, name):
        if name not in self.students:
            raise ValueError("Student not found")
        del self.students[name]

    def edit_student_name(self, old_name, new_name):
        if old_name not in self.students:
            raise ValueError("Student not found")
        if new_name in self.students:
            raise ValueError("New student name already exists")
        self.students[new_name] = self.students.pop(old_name)

    def add_course_to_student(self, student_name, course_name):
        if student_name not in self.students:
            raise ValueError("Student not found")
        self.students[student_name].add_course(course_name)

    def record_grade(self, student_name, course_name, grade):
        if student_name not in self.students:
            raise ValueError("Student not found")
        self.students[student_name].add_grade(course_name, grade)

    def mark_attendance(self, student_name, date, present):
        if student_name not in self.students:
            raise ValueError("Student not found")
        self.students[student_name].mark_attendance(date, present)

    def list_students(self):
        return list(self.students.keys())

    def find_student(self, name):
        return self.students.get(name, None)
