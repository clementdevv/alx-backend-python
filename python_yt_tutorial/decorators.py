# Python Decorator 

def operation_logger(func): 
    def wrapper (a,b): 
        print(f"Performing {func.__name__} on {a} and {b}")
        result = func(a,b)
        print(f"Result: {result}\n")
        return result 
    return wrapper 

@operation_logger
def addition(a,b):
    return a + b

@operation_logger 
def subtraction(a,b): 
    return a-b 

@operation_logger 
def multiplication(a,b): 
    return a*b 

@operation_logger
def division(a,b): 
    if b == 0:
        return "Cannot divide by zero"
    return a / b

#Run operation 
addition(10,5)
multiplication(45,5)
division(50,0)
subtraction(34,22)