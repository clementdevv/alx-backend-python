# Write a function that yields each lowercase letter in the English Alphabet
import string

def letters():
    for c in string.ascii_lowercase:
        yield c

for letter in letters(): 
    print(letter)