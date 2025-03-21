'''Class Employee 
{ string name;
  int age;
  float salary;

  public : string getName();
  void setName(string name);

  int getAge();
  void setAge(int age);

  float getSalary();
  void setSalary(float salary);
};

Employee employee;'''

# Is 'employee' an object or a data structure? Why?
'''Employee is a data structure as it exposes the data in private variables. It violates the abstraction in OOPS.'''

# Expressing employee as an Object


class Employee:
    def __init__(self, name, age, salary):
        # setting variables as private
        self._name = name
        self._age = age
        self._salary = salary

    def define_bonus(self):
        return self._age*100 + self._salary


employee = Employee("Rishabh", 25, 155000)
bonus = employee.define_bonus()
print(f'Employee bonus is {bonus}')
