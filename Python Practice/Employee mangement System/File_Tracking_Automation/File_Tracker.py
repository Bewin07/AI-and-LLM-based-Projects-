import os
import mysql.connector

class FileTracker:
    def __init__(self):
        self.latest_files = []
    def get_latest_files(self):
        os.chdir(r"C:\Users\imman\Documents\Python Practice\Python codes\Python codes\main folder")
        current_path = os.getcwd()
        for item in os.listdir(current_path):
            folder_path = os.path.join(current_path, item)
            if os.path.isdir(folder_path):
                files = os.listdir(folder_path)
                if files:
                    latest_file = max(
                        files,
                        key=lambda file: os.path.getmtime(
                            os.path.join(folder_path, file)
                        )
                    )
                    self.latest_files.append(latest_file)

        return self.latest_files

    def store_files(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rootbewin",
            database="automation"
        )

        cursor = conn.cursor()

        for file_name in self.latest_files:
            cursor.execute(
                "INSERT INTO files_table(filename) VALUES (%s)",
                (file_name,)
            )

        conn.commit()
        cursor.close()
        conn.close()

        print("Files stored successfully")

    def view_files(self):
        print("\nLatest Files Found:")
        print("-" * 30)

        for file_name in self.latest_files:
            print(file_name)

tracker = FileTracker()
tracker.get_latest_files()
tracker.view_files()
tracker.store_files()