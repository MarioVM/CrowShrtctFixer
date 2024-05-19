import concurrent.futures

def find_file_in_drive(drive: str, name: str) -> str:
  """
  Function to find a file in the given drive.
  
  Parameters:
  drive (str): The drive path to search in.
  name (str): The name of the file to find.

  Returns:
  str: The full path to the file if found, None otherwise.
  """
  # Use os.walk to iterate over each directory in the drive
  for root, dirs, files in os.walk(drive):
    # If the file is found, return its full path
    if name in files:
      return os.path.join(root, name)
  # If the file is not found, return None
  return None

def find_file(name: str, drives: list) -> str:
  """
  Function to find a file in the given drives.
  
  Parameters:
  name (str): The name of the file to find.
  drives (list): A list of drive paths to search in.

  Returns:
  str: The full path to the file if found, None otherwise.
  """
  # Use a ThreadPoolExecutor to parallelize the search
  with concurrent.futures.ThreadPoolExecutor() as executor:
    # Start a separate thread for each drive
    future_to_drive = {executor.submit(find_file_in_drive, drive, name): drive for drive in drives}
    # Wait for the threads to complete and gather the results
    for future in concurrent.futures.as_completed(future_to_drive):
      result = future.result()
      # If the file was found, return its path
      if result is not None:
        return result
  # If the file was not found in any of the drives, return None
  return None