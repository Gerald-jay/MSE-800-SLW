from dataclasses import dataclass

@dataclass
class Employee:
    name: str
    salary: float
    job_title: str

    def display_info(self) -> None:
        print(f"Name: {self.name}")
        print(f"Job Title: {self.job_title}")
        print(f"Salary: ${self.salary:,.2f}")
        print("-" * 32)

    def give_raise(self, amount: float | None = None, percent: float | None = None) -> None:
        if (amount is None) == (percent is None):
            raise ValueError("Provide exactly one of 'amount' or 'percent'.")

        if percent is not None:
            increment = self.salary * percent
        else:
            increment = amount

        if not isinstance(increment, (int, float)):
            raise ValueError("Increment must be a number")
        self.salary += increment
        if self.salary < 0:
            self.salary = 0.0

        print(f"{self.name} received a raise of ${increment:,.2f}. New salary: ${self.salary:,.2f}")

def main():
    emp1 = Employee(name="Alice", salary=8000.00, job_title="Software Engineer")
    emp2 = Employee(name="Eason", salary=7000.00, job_title="QA Analyst")

    print("Current Employees")
    emp1.display_info()
    emp2.display_info()

    print("Raises")
    emp1.give_raise(percent=0.15)
    emp2.give_raise(amount=600.00)

    print("\nUpdated Employees")
    emp1.display_info()
    emp2.display_info()

if __name__ == "__main__":
    main()
