import os
import pylnk3
import string

def find_file(name, drives):
    for drive in drives:
        for root, dirs, files in os.walk(drive):
            if name in files:
                return os.path.join(root, name)
    return None

def fix_shortcuts():
    home_dir = os.path.expanduser("~")
    drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]

    for foldername, subfolders, filenames in os.walk(home_dir):
        for filename in filenames:
            if filename.endswith('.lnk'):
                lnk_path = os.path.join(foldername, filename)
                lnk = pylnk3.LNK(lnk_path)
                if not os.path.exists(lnk.relative_path):
                    new_path = find_file(os.path.basename(lnk.relative_path), drives)
                    if new_path:
                        lnk.relative_path = new_path
                        lnk.working_dir = os.path.dirname(new_path)
                        lnk.save(lnk_path)

if __name__ == "__main__":
    fix_shortcuts()