# Import necessary modules
import os
import pylnk3
import string
import logging

def find_file(name: str, drives: list) -> str:
  """
  Function to find a file in the given drives.
  
  Parameters:
  name (str): The name of the file to find.
  drives (list): A list of drive paths to search in.

  Returns:
  str: The full path to the file if found, None otherwise.
  """
  # Iterate over each drive
  for drive in drives:
    # Use os.walk to iterate over each directory in the drive
    for root, dirs, files in os.walk(drive):
      # If the file is found, return its full path
      if name in files:
        return os.path.join(root, name)
  # If the file is not found, return None
  return None

def get_shortcuts_in_directory(directory: str) -> list:
  """
  Function to get all shortcuts in a directory.
  
  Parameters:
  directory (str): The directory to search in.

  Returns:
  list: A list of full paths to the shortcuts found.
  """
  # List to store the shortcuts
  shortcuts = []
  # Use os.walk to iterate over each directory in the directory and its subdirectories
  for foldername, subfolders, filenames in os.walk(directory):
    # Iterate over each file in the current directory
    for filename in filenames:
      # If the file is a shortcut
      if filename.endswith('.lnk'):
        # Get the full path to the shortcut
        lnk_path = os.path.join(foldername, filename)
        # Add the shortcut to the list
        shortcuts.append(lnk_path)
  # Return the list of shortcuts
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
    # Create a shortcut object
    lnk = pylnk3.LNK(lnk_path)
  except Exception as e:
    # Log the error and return
    logging.error(f"Error creating shortcut object for {lnk_path}: {str(e)}")
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

  # Iterate over each shortcut
  for shortcut in shortcuts:
    # Fix the shortcut
    fix_shortcut(shortcut, drives)

# If the script is run as a standalone program
if __name__ == "__main__":
  # Start the process of fixing broken shortcuts
  fix_shortcuts()