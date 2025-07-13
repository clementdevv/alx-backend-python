# Dunder/Magic Methods in Python - Map to specific kind of behaviors in Python

#__init__ method is used to define what happens when a new instance of an Object in OOP.
#the __init__ method is called a constructor and it is automatically called when a new instance of an object is created. 

class Rect: 
    def __init__ (self, x, y):
        self.x = x
        self.y = y 

r = Rect(2,3)
print(r.x, r.y)