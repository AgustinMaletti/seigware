import sys, os

print('Chose one option:\n 1- Run app\n 2- Test Aapp')
option = input('Enter an option: ')

if option == '1':
    print('Running next command')
    print('python app.py')
elif option== '2':
    print('Running next command')
    print('python test.py')
else:
    print('Please enter one available option')
