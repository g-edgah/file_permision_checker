import os
from pathlib import Path
import re
import stat




#handling input and path specified
def resolve_path(): 
    user_path = input(f"enter directory to scan \nexample: \n   absolute path: /etc/passwd \n   relative path: ../Downloads   \nleave blank or type '.' for current directory \n: ")

    current_dir = Path.cwd()
    relative_path = Path(user_path)
    resolved_path = relative_path.resolve()

    if not user_path:
        user_path = "."

    #handling relative paths
    if re.search(r'\.', user_path):
        #print("relative")
        #print (Path(resolved_path))
        if resolved_path.exists():
            print("path exists")
            path = resolved_path
        else:
            print(f"Error: {resolved_path} path doesn't exist")

    #handling absolute paths
    elif not re.search(r'\.', user_path):
        #print("not relative")
        #print (Path(user_path))

        if Path(user_path).exists():
            print("path exists")
            path = user_path
        else:
            print(f"Error: {user_path} doesn't exist")

    return path


#checking for world writable files
def check_writable(path):
    writable = []

    path = Path(path)
    
    if not path.is_dir():
        print(f"Error: {path} is not a directory")
        return []
    
    print(f"scanning for writable files in {path}\n")

    #scan directory recursively for files
    for file in path.rglob('*'):
        try:
            if file.is_file():
                file_stat = file.stat()
                permissions = file_stat.st_mode

                #bitwise & to check if world writable
                if permissions & stat.S_IWOTH:
                    writable.append(file)
                
        except (PermissionError, OSError) as e:
            print(f"cannot access {file} - {e}")

    return writable

#displaying the results
def results(writable):

    if not writable:
        print("no world writable files  found \n")
        return
    
    print(f"{len(writable)} world writable files found \n")
 

    for i, file in enumerate(writable, 1):
        try:
            file_stat = file.stat()
            permissions = oct(file_stat.st_mode)[-3:]
            size = file_stat.st_size
            owner = file.owner()

            print(f"{i:2d}. {file}")
            print(f"    Permissions: {permissions} \n    Size: {size:>8}bytes \n    Owner: {owner}")

        except OSError as e:
            print(f"{i:2d}. {file},- Error: {e}")

#bringing it all together
def main():
    path = resolve_path()
    writable = check_writable(path)
    results(writable)

main()
