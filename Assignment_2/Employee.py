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
    def load_employees(filename='.\\Inputs\\employees.csv'):
        try:
            employees = []
            with open(filename, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    employee = Employee(row[0], row[1], row[2], row[3] == 'TRUE')
                    employees.append(employee)
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
        return employees

    @staticmethod
    def save_employee(employee, filename='.\\Inputs\\employees.csv'):
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([employee.id, employee.name, employee.department, employee.working])
        EmployeeDatabase.load_employees()
        

    @staticmethod
    def refresh_employee_data(employees, filename='.\\Inputs\\employees.csv'):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            for emp in employees:
                writer.writerow([emp.id, emp.name, emp.department, emp.working])
        print(employees)


class EmployeeService:
    @staticmethod
    def terminate_employee(employee_id, filename='.\\Inputs\\employees.csv'):
        employees = EmployeeDatabase.load_employees(filename)
        employee_to_terminate = [emp for emp in employees if emp.id == employee_id][0]

        if employee_to_terminate:
            employee_to_terminate.working = False
            EmployeeDatabase.refresh_employee_data(employees, filename)
            print(f'Employee with id {employee_to_terminate.id}, {employee_to_terminate.name} terminated.')
            print(f'Working status of employee {employee_to_terminate.name} set to {employee_to_terminate.working}')
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

    print(f"Is Employee 4 working? {employees[2].is_working()}")
