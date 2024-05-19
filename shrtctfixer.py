import os
import pylnk
import string
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import time

# Cache dictionary to store search results
search_cache = {}

def find_file(name: str, drives: list) -> str:
    if name in search_cache:
        return search_cache[name]

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
                search_cache[name] = result
                return result
    search_cache[name] = None
    return None

def get_shortcuts_in_directory(directory: str) -> list:
    shortcuts = []
    for foldername, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.lnk'):
                lnk_path = os.path.join(foldername, filename)
                shortcuts.append(lnk_path)
    return shortcuts

def fix_shortcut(lnk_path: str, drives: list, progress_bar) -> None:
    try:
        lnk = pylnk.for_file(lnk_path)
    except Exception as e:
        logging.error(f"Error creating shortcut object for {lnk_path}: {str(e)}")
        tqdm.write(f"Error creating shortcut object for {lnk_path}: {str(e)}")
        progress_bar.update(1)
        return

    tqdm.write(f"Processing shortcut: {lnk_path}")

    if not os.path.exists(lnk.local_base_path):
        tqdm.write(f"Target file not found for shortcut: {lnk.local_base_path}")
        new_path = find_file(os.path.basename(lnk.local_base_path), drives)
        if new_path:
            logging.info(f"Changed {lnk_path} from {lnk.local_base_path} to {new_path}")
            tqdm.write(f"Changed {lnk_path} from {lnk.local_base_path} to {new_path}")
            lnk.local_base_path = new_path
            lnk.save(lnk_path)
        else:
            tqdm.write(f"Target file not found in any drives for shortcut: {lnk.local_base_path}")
    else:
        tqdm.write(f"Target file exists for shortcut: {lnk.local_base_path}")

    progress_bar.update(1)

def fix_shortcuts() -> None:
    home_dir = os.path.expanduser("~")
    all_drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]

    exclude_drives = input("Enter the drives to exclude, separated by commas (e.g., 'C,D'): ").upper().split(',')
    drives = [drive for drive in all_drives if drive[0] not in exclude_drives]

    logging.basicConfig(filename='changes.log', level=logging.INFO, format='%(asctime)s - %(message)s')

    shortcuts = get_shortcuts_in_directory(home_dir)
    tqdm.write(f"Found {len(shortcuts)} shortcuts to process")

    with tqdm(total=len(shortcuts), desc="Fixing Shortcuts") as progress_bar:
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(fix_shortcut, shortcut, drives, progress_bar) for shortcut in shortcuts]
            for future in as_completed(futures):
                future.result()

if __name__ == "__main__":
    start_time = time.time()
    fix_shortcuts()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Completed in {elapsed_time:.2f} seconds")
