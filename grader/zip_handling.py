import zipfile
import os

def rename(filename, uploadfile, dir):
    lst = filename.split('/')
    if len(lst)>1:
        lst[0] = dir+uploadfile[6:-4]
    else:
        lst.insert(0,dir+uploadfile[6:-4])
    return '/'.join(lst)

def unzip(zipname, dir="workdir"):
    print('unzip input', zipname)
    zipdata = zipfile.ZipFile(zipname)  # 'upload/1-10.zip'
    zipinfos = zipdata.infolist()
    for zipinfo in zipinfos:
        # This will do the renaming
        if(zipinfo.filename[:2] == '__'):
            continue
        zipinfo.filename = rename(zipinfo.filename, zipname, dir)
        print(zipinfo.filename)
        zipdata.extract(zipinfo)

    # with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        # zip_ref.extract(dir)
    files_existed, basedir = find_files(dir+zipname[6:-4])
    if files_existed:
        return basedir
    else:
        raise Exception("File not found error")

def find_files(dir):
    for fname in os.listdir(dir):
        if fname.endswith('.GTL'):
            print('find',dir)
            return True, dir
        elif os.path.isdir(os.path.join(dir,fname)):
            files_existed, basedir = find_files(os.path.join(dir,fname))
            if files_existed:
                return files_existed, basedir
    return False, ""
