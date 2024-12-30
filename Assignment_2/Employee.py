import csv


class Employee:
    def __init__(self, employee_id, name, department, working):
        self.id = int(employee_id)
        self.name = name
        self.department = department
        self.working = bool(working)

    def is_working(self):
        return self.working


class EmployeeDatabase:
    @staticmethod
    def load_employees(filename='employees.csv'):
        employees = []
        try:
            with open(filename, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    employee = Employee(row[0], row[1], row[2], row[3] == 'True')
                    employees.append(employee)
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
        return employees

    @staticmethod
    def save_employee(employee, filename='employees.csv'):
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([employee.id, employee.name, employee.department, employee.working])

    @staticmethod
    def refresh_employee_data(employees, filename='employees.csv'):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            for emp in employees:
                writer.writerow([emp.id, emp.name, emp.department, emp.working])


class EmployeeService:
    @staticmethod
    def terminate_employee(employee_id, filename='employees.csv'):
        employees = EmployeeDatabase.load_employees(filename)
        employee_to_terminate = next((emp for emp in employees if emp.id == employee_id), None)

        if employee_to_terminate:
            employee_to_terminate.working = False
            EmployeeDatabase.refresh_employee_data(employees, filename)
            print(f'Employee with id {employee_to_terminate.id}, {employee_to_terminate.name} terminated.')
        else:
            print(f"Employee with id {employee_id} not found.")


class EmployeeReport:
    @staticmethod
    def print_employee_detail_report_xml(employee):
        print(f"<id>{employee.id}</id>\n<name>{employee.name}</name>\n<department>{employee.department}</department>")

    @staticmethod
    def print_employee_detail_report_csv(employee):
        print(f"{employee.id},{employee.name},{employee.department},{employee.working}")


if __name__ == "__main__":
    employees = EmployeeDatabase.load_employees()

    for emp in employees:
        EmployeeReport.print_employee_detail_report_xml(emp)
        EmployeeReport.print_employee_detail_report_csv(emp)

    new_employee = Employee(4, 'Sejal Jain', 'HR', True)
    EmployeeDatabase.save_employee(new_employee)

    EmployeeService.terminate_employee(3)

    print(f"Is Employee 1 working? {employees[0].is_working()}")
