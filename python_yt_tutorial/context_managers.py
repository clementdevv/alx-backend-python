#Context manager - A Construct that allows for resource allocation and release precisely, even if an error occurs
#One can write their own context manager in 2 major ways: 
# - Using a Class with __enter__ and __exit__
# - Using contextlib, which is cleaner for simple scenarios

# Simple Context manager for a simple calculator 
class OperationContext:
    def __enter__(self): 
        print("Starting the operation...")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb): 
        print("Finished the operation. \n")
        return False
    
    def add(self, a, b): 
        print(f"Adding {a} + {b} = {a+b}")

    def subtract(self, a, b): 
        print(f"Subtracting {a} - {b} = {a-b}")
        
with OperationContext() as op: 
    op.add(5,3)
    op.subtract(10,4)