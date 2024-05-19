import os
import pylnk3
import string
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

def find_file(name: str, drives: list) -> str:
    """
    Function to find a file in the given drives using parallel search.
    
    Parameters:
    name (str): The name of the file to find.
    drives (list): A list of drive paths to search in.

    Returns:
    str: The full path to the file if found, None otherwise.
    """
    def search_drive(drive):
        for root, dirs, files in os.walk(drive):
            if name in files:
                return os.path.join(root, name)
        return None

    with ThreadPoolExecutor() as executor:
        future_to_drive = {executor.submit(search_drive, drive): drive for drive in drives}
        for future in as_completed(future_to_drive):
            result = future.result()
            if result:
                return result
    return None

def get_shortcuts_in_directory(directory: str) -> list:
    """
    Function to get all shortcuts in a directory.
    
    Parameters:
    directory (str): The directory to search in.

    Returns:
    list: A list of full paths to the shortcuts found.
    """
    shortcuts = []
    for foldername, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.lnk'):
                lnk_path = os.path.join(foldername, filename)
                shortcuts.append(lnk_path)
    return shortcuts

def fix_shortcut(lnk_path: str, drives: list) -> None:
    """
    Function to fix a single shortcut.
    
    Parameters:
    lnk_path (str): The full path to the shortcut.
    drives (list): A list of drive paths to search in for the target file.

    Returns:
    None

    Side effects:
    Modifies the shortcut file at lnk_path if the target file is found in the drives.
    Logs any changes made or errors encountered to a log file.
    """
    try:
        lnk = pylnk3.LNK(lnk_path)
    except Exception as e:
        logging.error(f"Error creating shortcut object for {lnk_path}: {str(e)}")
        return
    if not os.path.exists(lnk.relative_path):
        new_path = find_file(os.path.basename(lnk.relative_path), drives)
        if new_path:
            logging.info(f"Changed {lnk_path} from {lnk.relative_path} to {new_path}")
            lnk.relative_path = new_path
            lnk.working_dir = os.path.dirname(new_path)
            lnk.save(lnk_path)

def fix_shortcuts() -> None:
    """
    Function to fix broken shortcuts in the user's home directory.
    
    Parameters:
    None

    Returns:
    None

    Side effects:
    Asks the user for input.
    Modifies shortcut files in the user's home directory.
    Logs any changes made or errors encountered to a log file.
    """
    home_dir = os.path.expanduser("~")
    all_drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]

    exclude_drives = input("Enter the drives to exclude, separated by commas (e.g., 'C,D'): ").upper().split(',')
    drives = [drive for drive in all_drives if drive[0] not in exclude_drives]

    logging.basicConfig(filename='changes.log', level=logging.INFO, format='%(asctime)s - %(message)s')

    shortcuts = get_shortcuts_in_directory(home_dir)

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(fix_shortcut, shortcut, drives) for shortcut in shortcuts]
        for future in as_completed(futures):
            future.result()

if __name__ == "__main__":
    fix_shortcuts()
