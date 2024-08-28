import os
import shutil
import time

class BackupSystem:
    def __init__(self, backup_folder="backups"):
        self.backup_folder = backup_folder
        if not os.path.exists(backup_folder):
            os.makedirs(backup_folder)

    def create_backup(self, data_file="students.csv"):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        backup_filename = os.path.join(self.backup_folder, f"backup-{timestamp}.csv")
        shutil.copyfile(data_file, backup_filename)
        print(f"Backup created: {backup_filename}")

    def restore_backup(self, backup_file):
        shutil.copyfile(backup_file, "students.csv")
        print(f"Restored backup: {backup_file}")
