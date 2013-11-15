import os.path

def split_file_path(full_path):
    """Returns path, filename, file extension for a given full path."""
    path, filename = os.path.split(full_path)
    name, extension = os.path.splitext(filename)

    # make sure filenames are standardized
    extension = extension.lower()
    name = name.lower()

    return path, name, extension

