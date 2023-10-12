import random
import string

def generate_random_number():
    
    return ''.join(random.choice(string.digits) for _ in range(6))
