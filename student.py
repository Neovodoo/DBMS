class Student:
    
    def __init__(self, i: int, name: str = "", was_present: bool = False, group: int = 0, mark: float = 0):
        self.id = i
        self.name = name
        self.was_present = was_present
        self.group = group
        self.mark = mark

    def __str__(self):
        return f"{self.id};{self.name};{self.was_present};{self.group};{self.mark}\n"

    