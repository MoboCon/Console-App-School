import hashlib

class AuthSystem:
    def __init__(self):
        self.users = {
            "admin": hashlib.sha256("adminpass".encode()).hexdigest(),
            "profesor": hashlib.sha256("profesorpass".encode()).hexdigest()
        }
        self.current_user = None
        self.role = None

    def authenticate(self, username, password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if username in self.users and self.users[username] == password_hash:
            self.current_user = username
            self.role = "administrator" if username == "admin" else "profesor"
            return True
        else:
            return False

    def is_admin(self):
        return self.role == "administrator"

    def is_profesor(self):
        return self.role == "profesor"
