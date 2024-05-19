Broken Shortcut Fixer
ShrtctFixer is a Python script that fixes broken shortcuts in the user's home directory. It searches for the target files of the shortcuts in all drives except those specified by the user, and updates the shortcuts if the target files are found. It also logs the changes to a changes.log file in the root directory of the application.

📋 Requirements
Python 3
pylnk library
tqdm library

🛠️ Installation
Install Python 3 if you haven't already. You can download it from the official website.

Install the required libraries using pip:
pip install pylnk
pip install tqdm

🚀 Usage
Run the script in a Python environment. When prompted, enter the drives to exclude from the search, separated by commas (e.g., 'C,D').

python shrtctfixer.py

The script will prompt you to enter the drives you want to exclude from the search (e.g., C,D). After that, it will start the process of fixing broken shortcuts. It will search for the target files in all drives except the excluded ones and update the shortcuts with the new locations of the target files. The changes will be logged to a changes.log file in the root directory of the application.

📝 Example

Enter the drives to exclude, separated by commas (e.g., 'C,D'): C,D
Scanning for shortcuts...
Found 5 shortcuts.
Checking and fixing shortcuts...
Changed C:\Users\User\Desktop\Example.lnk from E:\OldPath\Example.exe to F:\NewPath\Example.exe
...
Process completed. Check changes.log for details.


Functions
find_file(name: str, drives: list) -> str: Finds a file in the given drives using parallel search with caching.
get_shortcuts_in_directory(directory: str) -> list: Gets all shortcuts in a directory.
fix_shortcut(lnk_path: str, drives: list, progress_bar) -> None: Fixes a single shortcut.
fix_shortcuts() -> None: Fixes broken shortcuts in the user's home directory.
Logging
The script logs any changes made or errors encountered to a file named changes.log.

Verbose Logging
The script also provides verbose logging to the console, showing detailed information about the processing of each shortcut. This is implemented using tqdm.write, which prints messages without interfering with the progress bar.

Performance
The script uses Python's concurrent.futures module to search for files and fix shortcuts in parallel, which can significantly speed up the process if there are many shortcuts or drives to search in. The total time taken is printed at the end.

Limitations
The script can only fix shortcuts that point to files, not directories. It also does not handle shortcuts with relative paths.

📄 License
This project is licensed under the terms of the GNU General Public License v3.0. See the LICENSE file for details.

© 2024 MarioVM