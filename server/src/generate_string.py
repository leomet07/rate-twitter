import random

chars = '`1234567890-qwertyuiop[]asdfghjklzxcvbnm,./()'
def generate_string(len):
    string  = ''.join(random.choice(chars) for i in range(len))
    return string

