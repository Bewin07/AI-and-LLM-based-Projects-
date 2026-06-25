class EmployeeManager:

    FILE_NAME = "employees.txt"

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def authenticate(self):
        return self.username == "admin" and self.password == "1212"

    def add_employee(self):

        if not self.authenticate():
            print("Access Denied")
            return

        emp_id = input("Enter Employee ID: ")
        name = input("Enter Employee Name: ")
        department = input("Enter Department: ")
        salary = input("Enter Salary: ")

        with open(self.FILE_NAME, "a") as file:
            file.write(f"{emp_id},{name},{department},{salary}\n")

        print("Employee Added Successfully")

    def view_employees(self):

        if not self.authenticate():
            print("Access Denied")
            return
        try:
            with open(self.FILE_NAME, "r") as file:
                print("\nEMPLOYEE LIST")
                print("-" * 70)
                print(
                    f"{'ID':<10}"
                    f"{'NAME':<20}"
                    f"{'DEPARTMENT':<20}"
                    f"{'SALARY':<10}"
                )
                print("-" * 70)
                for i in file:
                    emp_id, name, dept, salary = i.strip().split(",")
                    print(f"{emp_id:<10}" f"{name:<20}" f"{dept:<20}" f"{salary:<10}")

        except FileNotFoundError:
            print("No employee records found")

    def update_salary(self):
        if not self.authenticate():
            print("Access Denied")
            return
        emp_id_search = input("Enter Employee ID: ")
        new_salary = input("Enter New Salary: ")
        records = []
        found = False
        try:
            with open(self.FILE_NAME, "r") as file:
                for i in file:
                    emp_id, name, dept, salary = i.strip().split(",")
                    if emp_id == emp_id_search:
                        records.append(f"{emp_id},{name},{dept},{new_salary}\n")
                        found = True
                    else:
                        records.append(i)
            with open(self.FILE_NAME, "w") as file:
                file.writelines(records)

            if found:
                print("Salary Updated Successfully")
            else:
                print("Employee Not Found")

        except FileNotFoundError:
            print("No employee records found")

    def delete_employee(self):
        if not self.authenticate():
            print("Access Denied")
            return
        delete_id = input("Enter Employee ID to Delete: ")
        records = []
        found = False
        try:
            with open(self.FILE_NAME, "r") as file:
                for i in file:
                    emp_id, name, dept, salary = i.strip().split(",")
                    if emp_id != delete_id:
                        records.append(i)
                    else:
                        found = True
            with open(self.FILE_NAME, "w") as file:
                file.writelines(records)

            if found:
                print("Employee Deleted Successfully")
            else:
                print("Employee Not Found")

        except FileNotFoundError:
            print("No employee records found")
