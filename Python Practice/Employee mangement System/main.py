from employee_manager import EmployeeManager

username = input("Username: ")
password = input("Password: ")

manager = EmployeeManager(username, password)

while True:

    print("\n")
    print("1. Add Employee")
    print("2. View Employees")
    print("3. Delete Employee")
    print("4. Update Salary")
    print("5. Exit")

    choice = input("Enter Choice: ")

    if choice == "1":
        manager.add_employee()

    elif choice == "2":
        manager.view_employees()

    elif choice == "3":
        manager.delete_employee()

    elif choice == "4":
        manager.update_salary()

    elif choice == "5":
        print("Thank You")
        break

    else:
        print("Invalid Choice")