import sqlite3
import threading

conn = sqlite3.connect('exercise.db', check_same_thread=False)
lock = threading.Lock()

class User:

    def get_name(self):
        pass

    def age(self, current_year):
        pass


class User:

    def __init__(self, name, birthyear):
        self.name = name
        self.birthyear = birthyear

    def get_name(self):
        pass

    def age(self, current_year):
        pass


class User:

    def __init__(self, name, birthyear):
        self.name = name
        self.birthyear = birthyear

    def get_name(self):
        return self.name.upper()

    def age(self, current_year):
        age = current_year - self.birthyear
        return age

john = User(name="John" ,birthyear=1999)
john.age(current_year=2023)
