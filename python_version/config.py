import os

def exists_test(name):
    if os.path.isfile(name):
        return True
    else:
        return False