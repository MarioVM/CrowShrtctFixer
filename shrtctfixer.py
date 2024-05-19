# Import necessary modules
import os
import pylnk3
import string

def find_file(name, drives):
  """
  Function to find a file in the given drives
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

def fix_shortcuts():
  """
  Function to fix broken shortcuts
  """
  # Get the path to the user's home directory
  home_dir = os.path.expanduser("~")
  # Generate a list of all existing drives, excluding the C drive
  drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\") and d != 'C']

  try:
    # Open a log file to record changes
    with open('changes.log', 'w') as log_file:
      # Use os.walk to iterate over each directory in the home directory and its subdirectories
      for foldername, subfolders, filenames in os.walk(home_dir):
        # Iterate over each file in the current directory
        for filename in filenames:
          # If the file is a shortcut
          if filename.endswith('.lnk'):
            # Get the full path to the shortcut
            lnk_path = os.path.join(foldername, filename)
            try:
              # Create a shortcut object
              lnk = pylnk3.LNK(lnk_path)
            except Exception as e:
              # Log the error and continue with the next file
              log_file.write(f"Error creating shortcut object for {lnk_path}: {str(e)}\n")
              continue
            # If the target file of the shortcut does not exist
            if not os.path.exists(lnk.relative_path):
              # Find the target file in the drives
              new_path = find_file(os.path.basename(lnk.relative_path), drives)
              # If the target file is found
              if new_path:
                # Log the change
                log_file.write(f"Changed {lnk_path} from {lnk.relative_path} to {new_path}\n")
                # Update the target path and working directory of the shortcut
                lnk.relative_path = new_path
                lnk.working_dir = os.path.dirname(new_path)
                # Save the changes to the shortcut
                lnk.save(lnk_path)
  except Exception as e:
    print(f"Error: {str(e)}")

# If the script is run as a standalone program
if __name__ == "__main__":
  # Start the process of fixing broken shortcuts
  fix_shortcuts()