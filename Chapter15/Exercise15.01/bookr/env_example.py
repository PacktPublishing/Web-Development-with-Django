import os

# This will set the value since it's not already set
os.environ.setdefault('UNSET_VAR', 'UNSET_VAR_VALUE')

# This value will not be set since it's already passed
# in from the command line
os.environ.setdefault('SET_VAR', 'SET_VAR_VALUE')


print('UNSET_VAR:' + os.environ.get('UNSET_VAR', ''))
print('SET_VAR:' + os.environ.get('SET_VAR', ''))

# All these values were provided from the shell in some way
print('HOME:' + os.environ.get('HOME', ''))
print('VAR1:' + os.environ.get('VAR1', ''))
print('VAR2:' + os.environ.get('VAR2', ''))
print('VAR3:' + os.environ.get('VAR3', ''))
print('VAR4:' + os.environ.get('VAR4', ''))
