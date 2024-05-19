import os
import pylnk3
import string
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import time

# Cache dictionary to store search results
search_cache = {}

def find_file(name: str, drives: list) -> str:
    """
    Function to find a file in the given drives using parallel search with caching.
    
    Parameters:
    name (str): The name of the file to find.
    drives (list): A list of drive paths to search in.

    Returns:
    str: The full path to the file if found, None otherwise.
    """
    # Check if the file name is already in the cache
    if name in search_cache:
        return search_cache[name]

    def search_drive(drive):
        """
        Function to search for the file in a specific drive.
        
        Parameters:
        drive (str): The drive path to search in.

        Returns:
        str: The full path to the file if found in the drive, None otherwise.
        """
        for root, dirs, files in os.walk(drive):
            if name in files:
                return os.path.join(root, name)
        return None

    # Use ThreadPoolExecutor to search multiple drives in parallel
    with ThreadPoolExecutor() as executor:
        future_to_drive = {executor.submit(search_drive, drive): drive for drive in drives}
        for future in as_completed(future_to_drive):
            result = future.result()
            if result:
                # Cache the result before returning
                search_cache[name] = result
                return result
    # Cache the None result if the file is not found
    search_cache[name] = None
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

def fix_shortcut(lnk_path: str, drives: list, progress_bar) -> None:
    """
    Function to fix a single shortcut.
    
    Parameters:
    lnk_path (str): The full path to the shortcut.
    drives (list): A list of drive paths to search in for the target file.
    progress_bar (tqdm): The progress bar object to update.

    Returns:
    None

    Side effects:
    Modifies the shortcut file at lnk_path if the target file is found in the drives.
    Logs any changes made or errors encountered to a log file.
    """
    try:
        # Create a shortcut object
        lnk = pylnk3.LNK(lnk_path)
    except Exception as e:
        # Log the error and return
        logging.error(f"Error creating shortcut object for {lnk_path}: {str(e)}")
        progress_bar.update(1)
        return
    # If the target file of the shortcut does not exist
    if not os.path.exists(lnk.relative_path):
        # Find the target file in the drives
        new_path = find_file(os.path.basename(lnk.relative_path), drives)
        # If the target file is found
        if new_path:
            # Log the change
            logging.info(f"Changed {lnk_path} from {lnk.relative_path} to {new_path}")
            # Update the target path and working directory of the shortcut
            lnk.relative_path = new_path
            lnk.working_dir = os.path.dirname(new_path)
            # Save the changes to the shortcut
            lnk.save(lnk_path)
    progress_bar.update(1)

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
    # Get the path to the user's home directory
    home_dir = os.path.expanduser("~")
    
    # Generate a list of all existing drives
    all_drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]

    # Ask the user which drives to exclude
    exclude_drives = input("Enter the drives to exclude, separated by commas (e.g., 'C,D'): ").upper().split(',')
    
    # Generate a list of drives to include, excluding the specified drives
    drives = [drive for drive in all_drives if drive[0] not in exclude_drives]

    # Configure logging
    logging.basicConfig(filename='changes.log', level=logging.INFO, format='%(asctime)s - %(message)s')

    # Get all shortcuts in the home directory
    shortcuts = get_shortcuts_in_directory(home_dir)

    # Initialize the progress bar
    with tqdm(total=len(shortcuts), desc="Fixing Shortcuts") as progress_bar:
        # Use ThreadPoolExecutor to fix shortcuts in parallel
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(fix_shortcut, shortcut, drives, progress_bar) for shortcut in shortcuts]
            for future in as_completed(futures):
                future.result()

# If the script is run as a standalone program
if __name__ == "__main__":
    # Start the process of fixing broken shortcuts
    start_time = time.time()
    fix_shortcuts()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Completed in {elapsed_time:.2f} seconds")
