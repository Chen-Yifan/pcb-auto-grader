import zipfile
import os

def unzip(zip_file, dir="workdir"):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(dir)
    files_existed, basedir = find_files(dir)
    if files_existed:
        return basedir
    else:
        raise Exception("File not found error")

def find_files(dir):
    for fname in os.listdir(dir):
        if fname.endswith('.GTL'):
            return True, dir
        elif os.path.isdir(os.path.join(dir,fname)):
            files_existed, basedir = find_files(os.path.join(dir,fname))
            if files_existed:
                return files_existed, basedir
    return False, ""