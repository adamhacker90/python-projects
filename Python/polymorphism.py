# class Animal():
#     def speak(self):
#         raise NotImplementedError("Subclass needs to implement this method")

# class Dog(Animal):
#     def speak(self):
#         return "woof"

# class Cat(Animal):
#     def speak(self):
#         return "meow"

# class Fish(Animal):
#     pass

# d = Dog()
# print(d.speak())
# f = Fish()
# print(f.speak())





#special/magic methods

from copy import copy

class Human:
    def __init__(self, first, last, age):
        self.first = first
        self.last = last
        self.age = age
   
    def __repr__(self):
        return f"Human named {self.first} {self.last} aged {self.age}"

    def __len__(self):
        return self.age

    def __add__(self, other):
        if isinstance(other, Human):
            return Human(first='Newborn', last=self.last, age=0)
        return "You can't add that!"

    def __mul__(self, other):
        if isinstance(other, int):
            return [copy(self) for i in range(other)]
        return "Can't Multiply"


j = Human("Jenny", "Larsen", 47)
k = Human("Kevin", "Jones", 49)
# triplets = j * 3

# print(triplets)

triplets = (k + j) * 3 
triplets[0].first= 'Jessica'
triplets[1].first= 'James'
triplets[2].first= 'Joey'
print(triplets)