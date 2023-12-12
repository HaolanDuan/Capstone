import os
import mylib
import config

config = config.Config()
result = config.Result()

def exists_test(name):
    if os.path.isfile(name):
        return True
    else:
        return False

def assert_file_exist(desc, name):
    if not exists_test(name):
        print(desc + " " + name + "not found")
        exit(1)
