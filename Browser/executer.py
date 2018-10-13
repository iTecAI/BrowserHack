import os
os.chdir(os.getcwd())
try:
    exec(open(os.getcwd() + '\\bmain.py', 'r').read())
except FileNotFoundError:
    print('NoBrowser')
    
