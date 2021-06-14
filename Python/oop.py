
class User:
    active_users = 0

    @classmethod
    def display_active_users(cls):
        return f"There are currently {cls.active_users} active users"
    
    @classmethod
    def from_string(cls, dat_str):
        first,last,age = dat_str.split(",")
        return cls(first, last, int(age))

    def __init__(self, first, last, age):
        self.first = first
        self.last = last
        self.age = age
        User.active_users += 1

    def __repr__(self):
        return f"{self.first} is {self.age}"

    def logout(self):
        User.active_users -= 1
        return f"{self.first} has logged out"

    def full_name(self):
        return f"{self.first} {self.last}"

    def initials(self):
        return f"{self.first[0]}.{self.last[0]}"

    def likes(self, thing):
        return f"{self.first} likes {thing}"
        
    def is_senior(self):
        return self.age >= 65

    def birthday(self):
        self.age += 1
        return f"Happy {self.age}th Birthday, {self.first}"

class Moderator(User):
    total_mods = 0
    def __init__(self, first, last, age, community):
        super().__init__(first, last, age)
        self.community = community
        Moderator.total_mods += 1

    @classmethod
    def display_active_mods(cls):
        return f"There are currently {cls.total_mods} active moderators"

    def remove_post(self):
        return f"{self.full_name} removed a post from the {self.community}"

u1 = User("Tom", "Garcia", 35)
u2 = User("Tom", "Garcia", 35)
u3 = User("Tom", "Garcia", 35)
jasmine = Moderator("Jasmine", "O'conner", 61, "Piano")
jasmine = Moderator("Jasmine", "O'conner", 61, "Piano")
print(User.display_active_users())
print(Moderator.display_active_mods())


# tom = User.from_string("Tom,Jones,89")
# j = User('judy', 'steele', 18)

# print(tom.first)
# print(tom.full_name())
# print(tom.birthday())
# print(tom)
# print(j)



# user1 = User("Joe", "Schmo", 68)
# user2 = User("Blanca", "Lopez", 41)
# print(User.display_active_users())
# user1 = User("Joe", "Schmo", 68)
# user2 = User("Blanca", "Lopez", 41)
# print(User.display_active_users())
# print(User.active_users)
# print(user2.logout())
# print(User.active_users)


# print(user1.first, user1.last, user1.age)
# print(user2.first, user2.last, user2.age)
# print(user2.is_senior())
# print(user1.age)
# print(user1.birthday())
# print(user1.age)







# class Person:
#     def __init__(self):
#         self.name = "Tony"
#         self._secret = "hi!"
#         self.__msg = "I like turtles"
#         self.__lol = "HAHAHAHAHA"
# p = Person()

# # print(dir(p))
# print(p.name)
# print(p._secret)
# print(p.__msg)
# print(p._Person__msg)
# print(p._Person__lol)












# class Pet:
#     allowed = ['cat', 'dog', 'fish', 'rat']

#     def __init__(self, name, species):
#         if species not in Pet.allowed:
#             raise ValueError(f"You can't have a {species} pet!")
#         self.name = name
#         self.species = species

#     def set_species(self, species):
#         if species not in Pet.allowed:
#             raise ValueError(f"You can't have a {species} pet!")
#         self.species = species
# cat = Pet("Blue", "cat")
# dog = Pet("Wyatt", "dog")









# class Human:
#     def __init__(self, first, last, age):
#         self.first = first
#         self.last = last
#         if age >= 0:
#             self._age = age
#         else:
#             self._age = 0
    
#     @property
#     def age(self):
#         return self._age

#     @age.setter
#     def age(self, value):
#         if value >= 0:
#             self._age = value
#         else:
#             raise ValueError("age can't be negative")
    
#     @property
#     def full_name(self):
#         return f"{self.first} {self.last}"
    
    

# jane = Human("Jane", "Goodall", 50)

# print(jane.age)
# jane.age = 20
# print(jane.age)
# print(jane.full_name)










# class Animal:
#     def __init__(self, name, species):
#         self.name = name
#         self.species = species

#     def __repr__(self):
#         return f"{self.name} is a {self.species}"

#     def make_sound(self, sound):
#         print(f"this animal says {sound}")

# class Cat(Animal):
#     def __init__(self, name, breed, toy):
#         super().__init__(name, species="Cat")
#         self.breed = breed
#         self.toy = toy
#     def play(self):
#         print(f"{self.name} plays with {self.toy}")

# blue = Cat("Blue", "Scottish Fold", "String")
# print(blue)
# print(blue.species)
# print(blue.breed)
# print(blue.toy)
# blue.play()