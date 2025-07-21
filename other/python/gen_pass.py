from random import choice
from string import printable

#without signs
#custom_printable = [i for i in printable][0:62]
#full printable
custom_printable = [i for i in printable][0:94]
password_number = int(input('Enter the password number: '))
result = []

for _ in range(password_number):
    tmp = choice(custom_printable)
    result.append(tmp)

print(''.join(result))
