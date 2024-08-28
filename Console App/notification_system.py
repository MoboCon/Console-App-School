import smtplib
from email.mime.text import MIMEText

class NotificationSystem:
    def __init__(self, threshold_absences=3, threshold_grade=50):
        self.threshold_absences = threshold_absences
        self.threshold_grade = threshold_grade

    def send_email(self, to_address, subject, message):
        from_address = "your-email@example.com"
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = from_address
        msg["To"] = to_address

        with smtplib.SMTP("smtp.example.com", 587) as server:
            server.starttls()
            server.login(from_address, "your-password")
            server.sendmail(from_address, to_address, msg.as_string())

    def check_student(self, student):
        if len([date for date, present in student.attendance.items() if not present]) >= self.threshold_absences:
            self.send_email("parent@example.com", "Attendance Alert", f"{student.name} has too many absences.")
        for course in student.get_courses().values():
            if course.get_average() < self.threshold_grade:
                self.send_email("parent@example.com", "Grade Alert", f"{student.name} has a low average in {course.name}.")
