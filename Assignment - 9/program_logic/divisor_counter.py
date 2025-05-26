class DivisorCounter:
    def __init__(self, number: int):
        if number <= 0:
            raise ValueError("Input must be a positive integer.")
        self.number = number

    def count(self) -> int:
        return sum(1 for i in range(1, self.number + 1) 
                   if self.number % i == 0)
