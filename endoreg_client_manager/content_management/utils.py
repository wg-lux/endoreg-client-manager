
def find_files(directory, patterns):
    files = []
    for pattern in patterns:
        files.extend(directory.glob(pattern))
    return files