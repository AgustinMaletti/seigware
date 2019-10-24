import sys, os
import subprocess

print('Chose one option:\n 1- Run app\n 2- Test Aapp')
option = input('Enter an option: ')

if option == '1':
    print('Running next command')
    print('python app.py')
    subprocess.call(['python3', 'app.py'])

elif option== '2':
    print('Running next command')
    print('python test.py')
    subprocess.call(['python3','-m', 'unittest', 'test.Test_FakeClient'])
else:
    print('Please enter one available option')
