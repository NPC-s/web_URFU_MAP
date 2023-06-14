import os

def get_path_of_static_file(path):
    return os.path.dirname(__file__) + path.replace("/", "\\")