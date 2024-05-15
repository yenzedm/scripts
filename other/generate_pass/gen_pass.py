from random import choice
from string import printable


signs_and_letters = [i for i in printable][-7::-1]
password_number = int(input('Enter the password number: '))
result = []

for _ in range(password_number):
    tmp = choice(signs_and_letters)
    result.append(tmp)

print(''.join(result))
