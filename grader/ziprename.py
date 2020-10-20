import zipfile

# for debug: how to rename upziped file to the same name as input zip file
uploadfile = 'upload/3_czhou34.zip'
zipdata = zipfile.ZipFile(uploadfile)
zipinfos = zipdata.infolist()

def rename(filename, uploadfile,dir='workdir'):
    lst = filename.split('/')
    lst[0] = dir+uploadfile[6:-4]
    return '/'.join(lst)

# iterate through each file
for zipinfo in zipinfos:
    # This will do the renaming
    if(zipinfo.filename[:2]=='__'):
        continue
    print(zipinfo.filename)
    zipinfo.filename = rename(zipinfo.filename, uploadfile)
    zipdata.extract(zipinfo)
