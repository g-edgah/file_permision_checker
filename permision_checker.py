import os
import stat
import sys
from pathlib import Path

def check_writable(directory="."):
    writable = []

    directory = Path(directory)

    if not directory.exists():
        print(f"Error: {directory} does not exist")
        return []
    
    if not directory.is_dir():
        print(f"Error: {directory} is not a directory")
        return []
    
    print(f"scanning for writable files in {directory}")

    for file_path in directory.rglob('*'):
        try:
            if file_path.is_file():
                file_stat = file_path.stat()
                permissions = file_stat.st_mode

                if permissions & stat.S_IWOTH:
                    writable.append(file_path)
                
        except (PermissionError, OSError) as e:
            print(f"cannot access {file_path} - {e}")

    return writable

def results(writable):
    if not writable:
        print("no world writable files  found")
        return
    
    print(f"{len(writable)} world writable files found")
    print("")

    for i, file_path in enumerate(writable, 1):
        try:
            file_stat = file_path.stat()
            permissions = oct(file_stat.st_mode)[-3:]
            size = file_stat.st_size
            owner = file_path.owner()

            print(f"{i:2d}. {file_path}")
            print(f"    Permissions: {permissions} \n    Size: {size:>8}bytes \n    Owner: {owner}")

        except OSError as e:
            print(f"{i:2d}. {file_path},- Error: {e}")

def main():
    directory = sys.argv[1] if len(sys.argv) > 1 else "."

    writable = check_writable(directory)
    results(writable)

main()