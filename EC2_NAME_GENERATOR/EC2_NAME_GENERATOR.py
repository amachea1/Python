import random

print ('Welcome to EC2 Name Generator')
department = input ('Enter your department:')

allowed_departments = ['cloud engineering','finops']

if department.lower() in allowed_departments:
    count = int(input('How many names would your department like?'))

    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    for i in range(count):
        suffix = ''
        for j in range(6):
            suffix = suffix + random.choice(characters)
        print (department + '-' + suffix)

else: 
    print('Sorry, only Cloud Engineering and FinOps allowed.')